from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pypdf import PdfReader


@dataclass
class ParsedJD:
    source_path: str
    raw_text: str
    cleaned_text: str
    file_type: str  # "txt" | "pdf"


def _clean_text(text: str) -> str:
    # Minimal cleaning: normalize whitespace and remove repeated blank lines.
    lines = [ln.strip() for ln in text.splitlines()]
    # Drop empty runs
    cleaned_lines = []
    blank = False
    for ln in lines:
        if ln == "":
            if not blank:
                cleaned_lines.append("")
            blank = True
        else:
            cleaned_lines.append(ln)
            blank = False
    return "\n".join(cleaned_lines).strip() + "\n"


def parse_jd(path: str | Path) -> ParsedJD:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JD not found: {p}")

    ext = p.suffix.lower().lstrip(".")
    if ext == "txt":
        raw = p.read_text(encoding="utf-8", errors="ignore")
        cleaned = _clean_text(raw)
        return ParsedJD(str(p), raw, cleaned, "txt")

    if ext == "pdf":
        reader = PdfReader(str(p))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        raw = "\n".join(pages)
        cleaned = _clean_text(raw)
        return ParsedJD(str(p), raw, cleaned, "pdf")

    raise ValueError(f"Unsupported JD format: .{ext} (use .txt or .pdf)")