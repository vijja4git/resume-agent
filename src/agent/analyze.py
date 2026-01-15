from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class JDAnalysis:
    must_have: List[str]
    nice_to_have: List[str]
    domains: List[str]
    seniority_signals: List[str]
    raw_keywords: List[str]


# Lightweight vocabulary to bootstrap (you can expand)
SKILL_PATTERNS = [
    r"\bC\+\+\b",
    r"\bC\b",
    r"\bPython\b",
    r"\bLinux\b",
    r"\bembedded\b",
    r"\bfirmware\b",
    r"\bRTOS\b",
    r"\bI2C\b",
    r"\bSPI\b",
    r"\bUART\b",
    r"\bADC\b",
    r"\bDAC\b",
    r"\bGPIO\b",
    r"\bCI/?CD\b",
    r"\bGit\b",
    r"\bunit testing\b",
    r"\bTCP/IP\b",
    r"\bnetwork(ing)?\b",
    r"\bsecurity\b",
]

DOMAIN_PATTERNS = [
    r"\bnetworking\b",
    r"\bsecurity\b",
    r"\boperating systems\b",
    r"\bdrivers?\b",
    r"\bhardware[-\s]software integration\b",
]


def _unique_sorted(items: List[str]) -> List[str]:
    return sorted(list(dict.fromkeys([i.strip() for i in items if i.strip()])))


def analyze_jd(cleaned_text: str) -> JDAnalysis:
    text = cleaned_text

    # Seniority cues (very basic)
    seniority = []
    if re.search(r"\b(\d+)\+?\s+years\b", text, flags=re.IGNORECASE):
        seniority.append("years_experience")
    if re.search(r"\blead\b|\bmentor\b|\bownership\b", text, flags=re.IGNORECASE):
        seniority.append("leadership_ownership")

    # Extract skills/domains by regex hits
    raw_hits = []
    for pat in SKILL_PATTERNS:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            raw_hits.append(m.group(0))

    domains = []
    for pat in DOMAIN_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            # store the pattern label-ish
            domains.append(re.sub(r"\\b|\\", "", pat).strip("()?:+"))

    raw_keywords = _unique_sorted([h.upper() if h.lower() in ("c", "rtos") else h for h in raw_hits])

    # Simple must-have vs nice-to-have split using section heuristics
    must = []
    nice = []

    # If JD contains "Required" / "Preferred" sections, split roughly
    required_block = ""
    preferred_block = ""
    req_match = re.split(r"(?i)\brequired\b|\bminimum qualifications\b", text, maxsplit=1)
    if len(req_match) > 1:
        required_block = req_match[1]

    pref_match = re.split(r"(?i)\bpreferred\b|\bnice to have\b|\bbonus\b", text, maxsplit=1)
    if len(pref_match) > 1:
        preferred_block = pref_match[1]

    for kw in raw_keywords:
        # If keyword appears in preferred block, treat as nice-to-have
        if preferred_block and re.search(re.escape(kw), preferred_block, flags=re.IGNORECASE):
            nice.append(kw)
        else:
            must.append(kw)

    return JDAnalysis(
        must_have=_unique_sorted(must),
        nice_to_have=_unique_sorted(nice),
        domains=_unique_sorted(domains),
        seniority_signals=_unique_sorted(seniority),
        raw_keywords=raw_keywords,
    )


def analysis_to_json(analysis: JDAnalysis) -> str:
    return json.dumps(asdict(analysis), indent=2, sort_keys=True)