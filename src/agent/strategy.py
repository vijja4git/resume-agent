from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


@dataclass
class StrategyPick:
    item_id: str
    item_type: str  # "experience_highlight" | "project" | "skill_group"
    title: str
    score: float
    matched_keywords: List[str]
    matched_tech: List[str]
    source_path: str  # where it came from inside the inventory (human-readable)


@dataclass
class StrategyPlan:
    jd_keywords: List[str]
    top_experience: List[StrategyPick]
    top_projects: List[StrategyPick]
    notes: List[str]


def _norm(s: str) -> str:
    return s.strip().lower()


def _norm_set(items: List[str]) -> set[str]:
    return set(_norm(x) for x in items if isinstance(x, str) and x.strip())


def load_inventory(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Inventory not found: {p}")
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def _extract_highlights(inv: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any], str]]:
    """
    Returns tuples: (id, title, obj, source_path)
    """
    out = []
    for exp in inv.get("experience", []) or []:
        exp_id = exp.get("id", "exp_unknown")
        exp_title = exp.get("title", "Unknown Title")
        for hl in exp.get("highlights", []) or []:
            hl_id = hl.get("id", "hl_unknown")
            hl_title = hl.get("title", "Untitled Highlight")
            source_path = f"experience[{exp_id}:{exp_title}].highlights[{hl_id}:{hl_title}]"
            out.append((hl_id, hl_title, hl, source_path))
    return out


def _extract_projects(inv: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any], str]]:
    out = []
    for proj in inv.get("projects", []) or []:
        pid = proj.get("id", "proj_unknown")
        title = proj.get("name", "Untitled Project")
        source_path = f"projects[{pid}:{title}]"
        out.append((pid, title, proj, source_path))
    return out


def _score_item(jd_kw: set[str], tech_list: List[str], truth_list: List[str]) -> Tuple[float, List[str], List[str]]:
    tech_norm = _norm_set(tech_list or [])
    # also allow matches from "truth" sentences (fallback)
    truth_text = " ".join(truth_list or [])
    truth_norm_hits = set()
    for k in jd_kw:
        if k and k in _norm(truth_text):
            truth_norm_hits.add(k)

    matched = sorted(list((jd_kw & tech_norm) | truth_norm_hits))
    # Weighted score: tech matches count more than text hits
    tech_matches = sorted(list(jd_kw & tech_norm))
    score = (2.0 * len(tech_matches)) + (1.0 * (len(matched) - len(tech_matches)))
    return score, matched, tech_matches


def build_strategy_plan(
    inventory_path: str | Path,
    jd_analysis_path: str | Path,
    top_k_exp: int = 3,
    top_k_proj: int = 3,
) -> StrategyPlan:
    inv = load_inventory(inventory_path)

    jd_obj = json.loads(Path(jd_analysis_path).read_text(encoding="utf-8"))
    jd_keywords_raw = jd_obj.get("must_have", []) + jd_obj.get("nice_to_have", [])
    jd_kw = _norm_set(jd_keywords_raw)

    picks_exp: List[StrategyPick] = []
    for hl_id, title, hl, src in _extract_highlights(inv):
        tech = hl.get("tech", []) or []
        truth = hl.get("truth", []) or []
        score, matched, matched_tech = _score_item(jd_kw, tech, truth)
        picks_exp.append(
            StrategyPick(
                item_id=hl_id,
                item_type="experience_highlight",
                title=title,
                score=score,
                matched_keywords=matched,
                matched_tech=matched_tech,
                source_path=src,
            )
        )

    picks_proj: List[StrategyPick] = []
    for pid, title, proj, src in _extract_projects(inv):
        tech = proj.get("tech", []) or []
        truth = proj.get("truth", []) or []
        score, matched, matched_tech = _score_item(jd_kw, tech, truth)
        picks_proj.append(
            StrategyPick(
                item_id=pid,
                item_type="project",
                title=title,
                score=score,
                matched_keywords=matched,
                matched_tech=matched_tech,
                source_path=src,
            )
        )

    # Sort by score, then by number of matched keywords
    picks_exp.sort(key=lambda p: (p.score, len(p.matched_keywords)), reverse=True)
    picks_proj.sort(key=lambda p: (p.score, len(p.matched_keywords)), reverse=True)

    notes = [
        "Scoring: tech matches weighted higher than keyword matches found in truth text.",
        "Keywords are normalized (lowercased) to avoid duplicates like Embedded vs embedded.",
        "Next: Strategy output will feed Generation Node for bullet rewrites.",
    ]

    return StrategyPlan(
        jd_keywords=sorted(list(jd_kw)),
        top_experience=picks_exp[:top_k_exp],
        top_projects=picks_proj[:top_k_proj],
        notes=notes,
    )


def plan_to_json(plan: StrategyPlan) -> str:
    return json.dumps(asdict(plan), indent=2, sort_keys=True)