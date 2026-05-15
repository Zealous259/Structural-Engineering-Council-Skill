# CLAUDE.md — engineering-council

## Plugin overview

Simulates a senior multi-disciplinary engineering review panel of 10 engineers across 5 fields. Accepts any design or engineering input, runs structured phases (parallel analysis → dependency mapping → synthesis), outputs comprehensive technical feedback with annotated drawings and precedent references. No grading or voting — only feedback on what is missing, what is wrong, and how to improve.

---

## File structure

### Single source of truth files — edit only these

| File | What it controls |
|------|-----------------|
| `skills/engineering-council/SKILL.md` | Full orchestration logic: phase sequence, model selection, diagram pipeline, output assembly |
| `skills/engineering-council/references/council/00-council-head.md` | Council head facilitator identity and dependency mapping process |
| `skills/engineering-council/references/council/01-structural-logician.md` | Fazlur Rahman Khan — structural logician persona |
| `skills/engineering-council/references/council/02-structural-provocateur.md` | Cecil Balmond — structural provocateur persona |
| `skills/engineering-council/references/council/03-infrastructure-pioneer.md` | Isambard Kingdom Brunel — infrastructure pioneer persona |
| `skills/engineering-council/references/council/04-material-minimalist.md` | Robert Maillart — material minimalist persona |
| `skills/engineering-council/references/council/05-system-ecologist.md` | Buckminster Fuller — systems ecologist persona |
| `skills/engineering-council/references/council/06-performance-environmentalist.md` | Werner Sobek — performance environmentalist persona |
| `skills/engineering-council/references/council/07-thermal-strategist.md` | Willis Carrier — thermal strategist persona |
| `skills/engineering-council/references/council/08-holistic-integrator.md` | Ove Arup — holistic integrator persona |
| `skills/engineering-council/references/council/09-material-poet.md` | Peter Rice — material poet persona |
| `skills/engineering-council/references/council/10-lightweight-pioneer.md` | Frei Otto — lightweight pioneer persona |
| `skills/engineering-council/analysis-phase.md` | Prompt template for parallel analysis phase |
| `skills/engineering-council/dependency-phase.md` | Prompt template for cross-field dependency mapping |
| `skills/engineering-council/synthesis-phase.md` | Prompt template for final synthesis |
| `output-schema.json` | JSON Schema for all council output |

---

## Key rules for agents working here

- Edit `skills/engineering-council/SKILL.md` for orchestration changes. Never edit phase templates directly as a workaround for orchestration issues.
- Edit persona cards in `references/council/` for behavior changes to individual engineers. One card = one engineer = one source of truth.
- Council head (`00-council-head.md`) must never give engineering design opinions. If you edit the card, verify no domain bias is introduced.
- Persona cards are intentionally opinionated and will find fault in different ways. This is by design. Do not moderate their positions.
- Phase templates are static prompt prefixes. Variable content (briefs, prior phase outputs) is injected at runtime by SKILL.md.
- Diagrams in Phase 1 must be specific to the submitted project, not generic textbook diagrams. Precedent references are generic; project diagrams are not.
- The output contains NO score, NO grade, NO vote. Only: problems, missing elements, improvements, diagrams, precedents, priority ranking.
