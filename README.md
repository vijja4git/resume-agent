# Resume Agent — Autonomous AI for Resume Tailoring (LaTeX-safe)

An autonomous AI agent that streamlines resume tailoring:
- Inputs: a **Job Description** (PDF/TXT) + a **Master Resume Inventory**
- Workflow: **Analyze → Strategize → Generate**
- Output: **strict LaTeX** (compiles to PDF) optimized for ATS matching
- Guardrails: **no hallucinations**, every bullet must map to inventory items

---

## Why this exists
Tailoring a resume manually is slow and inconsistent. This project automates the process while enforcing:
- Truthfulness (no invented skills/metrics)
- Formatting stability (LaTeX stays valid)
- Role awareness (Embedded vs Data vs QA tailoring)

---

## Planned Architecture (MVP)
1. **Parse Node**: read JD (PDF/TXT) → clean text
2. **Analysis Node**: extract must-have skills, keywords, constraints
3. **Strategy Node**: select best matching inventory projects/experience
4. **Generation Node**: rewrite bullets with targeted keywords (truth-checked)
5. **LaTeX Node**: render into fixed template, compile check

---

## Repo Structure (initial)