#!/usr/bin/env python3
"""Render application submitted-resume markdown and compact PDFs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from xml.sax.saxutils import escape

from pipeline_common import (
    IC_RESUME_PATH,
    REPO_ROOT,
    clean_text,
    load_applications,
    repo_relative,
    resume_source_path_for_role,
    save_json,
)


MANIFEST_PATH = REPO_ROOT / "applications" / "resumes" / "submission-manifest.json"
PROOF_LINE = (
    "Built and operated 0->1 systems at scale including $240M/month payments infrastructure, "
    "approximately $6M annualized observability cost reduction, and enterprise-grade SaaS systems "
    "on Salesforce Hyperforce."
)


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip()
    return text.lstrip()


def front_matter(app: dict) -> str:
    app_id = app["application_id"]
    title = f"Rohit Verma - {clean_text(app.get('company'))} - {clean_text(app.get('role'))} Resume"
    return "\n".join(
        [
            "---",
            "layout: resume",
            f"title: {title}",
            f"permalink: /applications/resumes/{app_id}/submitted/",
            "---",
            "",
        ]
    )


def current_resume_with_theme(app: dict) -> str:
    source_path = resume_source_path_for_role(app.get("role"))
    body = strip_front_matter(source_path.read_text(encoding="utf-8"))
    if source_path != IC_RESUME_PATH:
        return body

    lines = body.splitlines()
    theme = app.get("resume_theme") or {}
    positioning = clean_text(theme.get("positioning")) or clean_text(app.get("fit_reason"))
    if not positioning:
        return body

    experience_at = next((index for index, line in enumerate(lines) if line == "## Experience"), None)
    if experience_at is None:
        return body
    header = lines[:5]
    themed = header + ["", positioning, PROOF_LINE, ""] + lines[experience_at:]
    return "\n".join(themed).strip() + "\n"


def normalize_pdf_text(value: str) -> str:
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
        "\u2192": "->",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def styles():
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "ResumeH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=8.4,
            alignment=TA_CENTER,
            spaceAfter=1.5,
        ),
        "h2": ParagraphStyle(
            "ResumeH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=10.2,
            textColor=colors.HexColor("#111111"),
            borderWidth=0,
            spaceBefore=4,
            spaceAfter=2,
        ),
        "h3": ParagraphStyle(
            "ResumeH3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=8.4,
            leading=9.2,
            spaceBefore=3,
            spaceAfter=1,
        ),
        "h4": ParagraphStyle(
            "ResumeH4",
            parent=base["Heading4"],
            fontName="Helvetica-BoldOblique",
            fontSize=7.7,
            leading=8.5,
            spaceBefore=2.5,
            spaceAfter=1,
        ),
        "body": ParagraphStyle(
            "ResumeBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.25,
            leading=8.05,
            alignment=TA_LEFT,
            spaceAfter=1.4,
        ),
        "bullet": ParagraphStyle(
            "ResumeBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=6.95,
            leading=7.65,
            leftIndent=9,
            firstLineIndent=-5,
            bulletIndent=0,
            spaceAfter=0.8,
        ),
    }


def inline_markup(value: str) -> str:
    value = escape(normalize_pdf_text(value))
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return value


def story_from_markdown(markdown: str):
    st = styles()
    flow = []
    lines = strip_front_matter(markdown).splitlines()
    after_h1_contacts = 0
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            flow.append(Paragraph(inline_markup(" ".join(paragraph)), st["body"]))
            paragraph.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_paragraph()
            continue
        if line.startswith("# "):
            flush_paragraph()
            flow.append(Paragraph(inline_markup(line[2:]), st["h1"]))
            after_h1_contacts = 2
        elif after_h1_contacts > 0 and not line.startswith("#"):
            flush_paragraph()
            flow.append(Paragraph(inline_markup(line), st["contact"]))
            after_h1_contacts -= 1
        elif line.startswith("## "):
            flush_paragraph()
            flow.append(Paragraph(inline_markup(line[3:]), st["h2"]))
        elif line.startswith("### "):
            flush_paragraph()
            flow.append(Paragraph(inline_markup(line[4:]), st["h3"]))
        elif line.startswith("#### "):
            flush_paragraph()
            flow.append(Paragraph(inline_markup(line[5:]), st["h4"]))
        elif line.startswith("- "):
            flush_paragraph()
            flow.append(Paragraph(inline_markup(line[2:]), st["bullet"], bulletText="-"))
        else:
            paragraph.append(line)
    flush_paragraph()
    flow.append(Spacer(1, 1))
    return flow


def render_pdf(markdown: str, output_path: Path, title: str) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.38 * inch,
        leftMargin=0.38 * inch,
        topMargin=0.36 * inch,
        bottomMargin=0.34 * inch,
        title=title,
        author="Rohit Verma",
    )
    doc.build(story_from_markdown(markdown))


def pdf_page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(path)).pages)
    except Exception:
        return 0


def selected_applications(args) -> list[dict]:
    data = load_applications()
    apps = data.get("applications", [])
    selected_ids = set(args.application_id or [])
    if selected_ids:
        return [app for app in apps if app.get("application_id") in selected_ids]
    if args.approved_only:
        return [app for app in apps if app.get("status") == "approved"]
    return apps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--application-id", action="append", help="Application id to render; can be repeated")
    parser.add_argument("--approved-only", action="store_true", help="Render all approved applications")
    args = parser.parse_args()

    apps = selected_applications(args)
    manifest = []
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_app_id = {row.get("application_id"): row for row in manifest if isinstance(row, dict)}

    rendered = []
    for app in apps:
        app_id = clean_text(app.get("application_id"))
        resume_snapshot = clean_text(app.get("resume_snapshot_path"))
        if not app_id or not resume_snapshot:
            continue
        snapshot_path = REPO_ROOT / resume_snapshot
        output_dir = snapshot_path.parent
        submitted_md = output_dir / "submitted-resume.md"
        submitted_pdf = output_dir / "submitted-resume.pdf"

        resume_body = current_resume_with_theme(app)
        markdown = front_matter(app) + resume_body
        snapshot_markdown = front_matter({**app, "application_id": app_id}).replace("/submitted/", "/") + resume_body
        snapshot_path.write_text(snapshot_markdown, encoding="utf-8")
        submitted_md.write_text(markdown, encoding="utf-8")
        render_pdf(markdown, submitted_pdf, f"Rohit Verma - {app.get('company')} - {app.get('role')} Resume")
        pages = pdf_page_count(submitted_pdf)

        entry = {
            "application_id": app_id,
            "company": app.get("company"),
            "role": app.get("role"),
            "source_url": app.get("source_url"),
            "submitted_resume_md": repo_relative(submitted_md),
            "submitted_resume_pdf": repo_relative(submitted_pdf),
            "pages": pages,
        }
        by_app_id[app_id] = entry
        rendered.append(entry)

    save_json(MANIFEST_PATH, sorted(by_app_id.values(), key=lambda row: row.get("application_id") or ""))
    print(json.dumps({"rendered": len(rendered), "applications": rendered}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
