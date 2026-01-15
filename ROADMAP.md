# Autonomous AI Resume Tailoring Agent — Roadmap

## Project Status
**Current Phase:** Phase 0 — Foundation  
**Last Updated:** Day 1  
**Owner:** Cherish Teja Vijjagiri

---

## Project Goal
Build an autonomous AI agent that:
- Takes a Job Description + Master Resume Inventory
- Analyzes requirements and context
- Selects relevant experience
- Rewrites resume bullets for ATS optimization
- Outputs **strictly valid LaTeX** that compiles into a professional PDF
- Never hallucinates skills or experience

---

## Phase Breakdown

### Phase 0 — Foundation (IN PROGRESS)
- [x] Define project architecture
- [x] Define agent workflow (analysis → strategy → generation)
- [x] Decide language: Python
- [x] Decide output format: LaTeX
- [ ] Initialize Git repository
- [ ] Push first commit to GitHub
- [ ] Create master resume inventory schema
- [ ] Lock LaTeX template

---

### Phase 1 — MVP (NOT STARTED)
- [ ] Job Description parser (PDF / TXT)
- [ ] Keyword & must-have extractor
- [ ] Project/experience selector
- [ ] Bullet point rewriter
- [ ] LaTeX renderer
- [ ] End-to-end CLI (`python tailor.py`)

---

### Phase 2 — Agent Reliability
- [ ] Structured JSON outputs
- [ ] Hallucination guardrails
- [ ] Inventory-to-bullet traceability
- [ ] Validation & compile checks

---

### Phase 3 — Context Awareness
- [ ] Role classification (Embedded / Data / QA / General)
- [ ] Contextual project retrieval
- [ ] Multiple LaTeX templates

---

### Phase 4 — CI/CD Automation
- [ ] GitHub Actions trigger on new JD
- [ ] Auto-generate PDF
- [ ] Upload artifacts

---

## Design Rules (Non-Negotiable)
1. The agent **cannot invent skills**
2. All bullets must map to resume inventory
3. Output must be valid LaTeX
4. Resume formatting is fixed and versioned
5. AI outputs are structured, not free-form

---

## Next Immediate Action
✅ Initialize Git repository  
✅ Push initial commit with ROADMAP.md