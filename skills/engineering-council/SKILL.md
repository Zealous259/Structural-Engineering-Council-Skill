---
name: engineering-council
description: >
  Multi-disciplinary engineering review panel. 10 engineers across 5 fields analyze any design or
  engineering input through distinct technical lenses: parallel analysis with technical drawings,
  cross-field dependency mapping, synthesis report. No grading — only feedback on problems,
  missing elements, improvements. All output includes annotated technical diagrams (ASCII details
  + Mermaid system diagrams) and precedent references. Accepts any input: text, images, 3D file
  references, drawings, design descriptions.
---

# Engineering Council — Orchestration Skill

## Section 1: Overview

The Engineering Council is a structured multi-agent review process in which 10 engineers — each operating from a distinct technical field and professional framework — analyze a submitted design, produce annotated technical drawings of their specific concerns, and link their findings into cross-field dependency chains showing how one engineer's problem affects another's domain. Invoke this skill whenever a design artifact, structural scheme, building system, material strategy, or engineering question requires rigorous technical review from multiple disciplines simultaneously.

**This skill does not grade, score, or vote.** Output is feedback only: problems found, elements missing, improvements required, and the order in which to address them.

Output is a formatted PDF report written to the user's current working directory.

---

## Section 2: Input Handling

### Accepted Input Formats

- Freeform text descriptions of a design, structure, or system
- Images (via file paths — read and describe visual content before dispatching subagents)
- Sketches, plans, sections, or detail drawings (describe what is visible: geometry, dimensions, connections, materials)
- Rhino, Houdini, Grasshopper, Revit, or other 3D/BIM file references (note: Claude cannot directly parse binary files; reason about referenced geometry based on any descriptions provided; if key structural or system logic is ambiguous, ask the user to describe it before proceeding)
- Program documents, briefs, structural reports, specifications
- Any combination of the above

### Handling Images and 3D Models

**If the user provides an IMAGE of a design, 3D model, plan, or section:**
Describe what is visually present before briefing — geometry, structural elements, material palette, connections visible, system routing if legible. Include this description in the normalized brief. Engineers will annotate their concern diagrams with positional references to the image content.

**If the user provides a 3D FILE REFERENCE only (no image):**
Engineers generate abstracted 2D plan / section / axonometric ASCII diagrams representing their key concerns. These diagrams are generated from the description in the brief, not from the file itself.

**If the user provides a 2D DRAWING (plan, section, detail):**
Describe what is legible: geometry, dimensions shown, materials annotated, any visible structural logic. Engineers will generate parallel drawings showing what is missing or wrong relative to the provided drawing.

### Brief Normalization (mandatory before Phase 1)

Before dispatching any subagent, normalize all input into a single structured paragraph — the **normalized brief** — covering:

1. Work type (structural system, building, pavilion, bridge, product, detail, MEP scheme, etc.)
2. Scale, program, and context (physical, climatic, user requirements)
3. Structural and material logic (what is carrying loads, what is spanning, what materials are used or proposed)
4. Building systems proposed or implied (thermal, moisture, structural, services, envelope)
5. Constraints (code, budget, site, fabrication method, client requirements)
6. If images or drawings provided: visible geometry, connections, and any dimensional information legible in the input
7. **BCA occupancy classification** (Class 1–10) — determine from the program if possible (e.g. Class 6 = shop/café, Class 9b = assembly/school/pool, Class 10a = non-habitable structure/pavilion, Class 1 = house). If the class is ambiguous or the brief is insufficient, note "BCA class not determinable from brief" — do not guess.

**Output the normalized brief visibly to the user and wait for confirmation before proceeding to Phase 1.** Label it clearly:

> **Normalized Brief (confirm before council session begins):**
> [brief paragraph here]

The normalized brief is appended as the final item in every subagent prompt. Do not modify it after confirmation.

---

## Section 3: Default Roster

| ID | Name | Field | Role |
|----|------|-------|------|
| council-head | Dr. Sarah Chen | Process Facilitation | Council Facilitator (no engineering opinions) |
| structural-logician | Fazlur Rahman Khan | Structural Engineering | Force efficiency, load paths, structural legibility |
| structural-provocateur | Cecil Balmond | Structural Engineering | Informal geometry, structure as spatial generator |
| infrastructure-pioneer | Isambard Kingdom Brunel | Civil / Infrastructure | Ambition, material limits, buildability at scale |
| material-minimalist | Robert Maillart | Civil / Concrete | Minimum material, force follows form, concrete efficiency |
| system-ecologist | R. Buckminster Fuller | Environmental / Systems | Whole-earth thinking, synergetics, doing more with less |
| performance-environmentalist | Werner Sobek | Environmental / Sustainable | Triple-zero performance, lifecycle, material efficiency |
| thermal-strategist | Willis Carrier | Building Services / Mechanical | Thermal comfort, psychrometrics, HVAC systems |
| holistic-integrator | Ove Arup | Building Services / Integration | Comprehensive building engineering, architect-engineer collaboration |
| material-poet | Peter Rice | Materials / Fabrication | Material innovation, expressive tectonics, craft at scale |
| lightweight-pioneer | Frei Otto | Materials / Lightweight Structures | Tensile structures, form-finding, minimal surfaces |

Roster is configurable — see Section 8 for swapping instructions.

---

## Section 4: Phase Execution

This section is the authoritative execution guide for the controller Claude instance. Follow it precisely. All subagent dispatches use the Agent tool.

---

### Phase 0 — Brief Normalization

1. Read all user input.
2. If images are attached, describe visual content: geometry, visible structural elements, material palette, connections, any legible dimensions.
3. If 3D file paths are referenced, note them. If structural or system logic is unclear, ask the user to describe it before proceeding.
4. Write the normalized brief (one structured paragraph, covering all 6 elements listed in Section 2).
5. Output it visibly with the label above.
6. Wait for user confirmation. If the user confirms or makes no objection, proceed. If they correct or expand: update the brief and confirm again.

Do not dispatch any subagent until the normalized brief is confirmed.

---

### Phase 1 — Parallel Engineering Analysis

**Read** all 10 engineer persona cards:
- `references/council/01-structural-logician.md`
- `references/council/02-structural-provocateur.md`
- `references/council/03-infrastructure-pioneer.md`
- `references/council/04-material-minimalist.md`
- `references/council/05-system-ecologist.md`
- `references/council/06-performance-environmentalist.md`
- `references/council/07-thermal-strategist.md`
- `references/council/08-holistic-integrator.md`
- `references/council/09-material-poet.md`
- `references/council/10-lightweight-pioneer.md`

**Read** `analysis-phase.md`.

**Dispatch 10 subagent calls simultaneously** (single message, all 10 Agent tool calls in parallel).

Each subagent prompt contains, in this order:
1. Full content of the engineer's persona card
2. Full content of `analysis-phase.md`
3. The normalized brief

Model: `claude-sonnet-4-6` for each.

**Collect** all 10 JSON responses. Parse and store as the Phase 1 analysis array. Each response is a JSON object with fields: `id`, `field`, `engineer`, `severity_overall`, `summary`, `problems`, `missing_elements`, `improvements`, `compliance_flags`, `diagram`, `precedent`.

If any subagent returns malformed JSON: re-dispatch that subagent once with the same prompt before continuing.

---

### Phase 2 — Cross-Field Dependency Mapping

Persona cards were read in Phase 1 and remain in context — include the council head card in this prompt without re-reading from disk.

**Read** `references/council/00-council-head.md`.

**Read** `dependency-phase.md`.

**Dispatch 1 subagent** (council head) with:
1. Full content of `references/council/00-council-head.md`
2. Full content of `dependency-phase.md`
3. All 10 Phase 1 analysis JSONs (full objects, concatenated)
4. The normalized brief

Model: `claude-haiku-4-5-20251001`.

The council head returns a dependency map JSON with: `concern_chains` (arrays of linked engineer concerns where one field's problem directly affects another's), `systemic_gaps` (issues no single field caught but multiple fields hint at), and `dependency_diagram` (a Mermaid graph showing concern chains).

Store the dependency map. Proceed to Phase 3.

---

### Phase 3 — Synthesis Report

**Read** `synthesis-phase.md`.

**Dispatch 1 subagent** (council head) with:
1. Full content of `references/council/00-council-head.md`
2. Full content of `synthesis-phase.md`
3. All 10 Phase 1 analysis JSONs (full objects)
4. The Phase 2 dependency map JSON (full object)
5. The normalized brief

Model: `claude-opus-4-7`.

Collect synthesis JSON with fields: `status`, `executive_summary`, `critical_issues`, `major_issues`, `minor_issues`, `improvement_roadmap`, `compliance_summary`.

---

### Phase 4 — Report Assembly and PDF Export

Assemble all collected phase data into a structured Markdown report, write it to a file in the user's current project directory, then convert to PDF using pandoc and wkhtmltopdf.

#### Step 4a — Generate session ID and filename

Generate a session ID: 8 random hex characters (e.g. `b7e2a41f`). This is the short ID used in the filename.

Filename base: `engineering-council-review-<session_id>` (e.g. `engineering-council-review-b7e2a41f`).

Output files (written to the user's current working directory, or `~/Documents/` if the working directory is not writable):
- `engineering-council-review-<session_id>.md` — the Markdown report (intermediate)
- `engineering-council-review-<session_id>.pdf` — the final output

#### Step 4b — Assemble Markdown report

Write the following Markdown report to `engineering-council-review-<session_id>.md`.

````markdown
# Engineering Council Review

**Project:** [normalized brief — first sentence or up to 120 characters]
**Session:** [session_id] | [current date and time, formatted: DD Month YYYY, HH:MM]
**Status:** [READY FOR ITERATION | NEEDS SIGNIFICANT REWORK | REQUIRES REDESIGN]

> Status is not a grade. READY FOR ITERATION = problems are addressable within current design direction. NEEDS SIGNIFICANT REWORK = structural or systems strategy requires revision. REQUIRES REDESIGN = fundamental approach has engineering conflicts that cannot be resolved by iteration alone.

---

## Brief

[Full normalized brief paragraph]

---

## Council

| Engineer | Field | Lens |
|----------|-------|------|
| Dr. Sarah Chen | Process Facilitation | Neutral facilitator — no engineering opinions |
| Fazlur Rahman Khan | Structural Engineering | Force efficiency, load path legibility |
| Cecil Balmond | Structural Engineering | Structural geometry as spatial generator |
| Isambard Kingdom Brunel | Civil / Infrastructure | Buildability, ambition, material limits |
| Robert Maillart | Civil / Concrete | Minimum material, force follows form |
| R. Buckminster Fuller | Environmental / Systems | Whole-systems thinking, synergetics |
| Werner Sobek | Environmental / Sustainable | Triple-zero performance, lifecycle |
| Willis Carrier | Building Services | Thermal comfort, HVAC systems |
| Ove Arup | Building Services / Integration | Holistic building engineering |
| Peter Rice | Materials / Fabrication | Material innovation, expressive tectonics |
| Frei Otto | Materials / Lightweight | Tensile structures, form-finding |

---

## Phase 1 — Engineering Analyses

[For each of the 5 fields, in this order: Structural, Civil, Environmental, Building Services, Materials:]

### [Field Name]

---

#### [Engineer Name] — [severity_overall: CRITICAL | MAJOR | MINOR]

[summary field — written in the engineer's voice]

**Problems Identified**

[problems as numbered list: "severity: issue — location"]

**Missing Elements**

[missing_elements as numbered list: "element — impact"]

**Improvements Required**

[improvements as numbered list: "action — rationale"]

**Technical Diagram**

[diagram title]
[diagram description — 1 sentence]

[If diagram.type == "ascii": render as a plain code block (no language tag)]
[If diagram.type == "mermaid": render as a mermaid code block with ```mermaid language tag]

[Either:]
```
[diagram content — ASCII art, raw text, use diagram.content string with \n resolved to actual newlines]
```

[Or:]
```mermaid
[diagram content — Mermaid graph code, use diagram.content string with \n resolved to actual newlines]
```

**Precedent Reference**

> **[project]** — [engineer_architect], [year]
> **Principle:** [principle]
> **Study:** [what_to_study]

**NCC / Australian Standards Compliance**

[If compliance_flags is empty: "*No compliance issues identified by this engineer.*"]

[If compliance_flags is not empty: render as a table:]

| Standard | Clause | Issue | Severity |
|----------|--------|-------|----------|
[For each flag: | [standard] | [clause] | [issue] | [severity: NON-COMPLIANT | NEEDS VERIFICATION | ADVISORY] |]

---

[repeat for second engineer in this field]

[repeat for all 5 fields]

---

## Phase 2 — Cross-Field Dependency Chains

*Dr. Sarah Chen, Council Facilitator, has mapped the following concern chains — where one engineer's finding directly affects another engineer's domain.*

[dependency_diagram — rendered as mermaid code block]

```mermaid
[dependency_diagram.content]
```

[For each concern chain in concern_chains:]

### Chain [chain_id]: [chain_title] — [combined_severity: CRITICAL | MAJOR | MINOR]

[For each link in this chain:]
**[engineer_id]:** [concern_summary]
→ *affects:* [affects_next]

[next link]

[If systemic_gaps is not empty:]
### Systemic Gaps

*Issues that no single field caught in isolation but which emerge from the combination of findings:*

[systemic_gaps as bullet list]

---

## Phase 3 — Priority Feedback

### Summary

[executive_summary]

### Critical Issues

*Must be resolved before advancing to the next design stage.*

[critical_issues as numbered list]

### Major Issues

*Must be resolved before documentation or construction.*

[major_issues as numbered list]

### Minor Issues

*Should be resolved; will compound if left unaddressed.*

[minor_issues as numbered list]

---

## Improvement Roadmap

*Ordered by priority. Each step references the engineering field responsible.*

| Step | Action | Field | When |
|------|--------|-------|------|
[For each step in improvement_roadmap:]
| [step] | [action] | [field] | [priority] |

---

## NCC / BCA Compliance Register

**BCA Occupancy Class:** [compliance_summary.bca_class]

### Non-Compliant Items

*Must be resolved. These items represent clear conflicts with mandatory NCC/BCA or Australian Standard requirements.*

[If compliance_summary.non_compliant is empty: "*No non-compliant items identified.*"]
[Otherwise: numbered list of non_compliant items]

### Needs Verification

*Cannot be confirmed compliant from the information provided. Obtain confirmation before proceeding.*

[If compliance_summary.needs_verification is empty: "*All reviewable items confirmed or no verification required.*"]
[Otherwise: numbered list of needs_verification items]

### Advisory

*Meets minimum code requirements but falls short of best practice for this building type or use.*

[If compliance_summary.advisory is empty: "*No advisory items.*"]
[Otherwise: numbered list of advisory items]

---

## Precedents Index

*All precedent references cited by council members.*

[For each engineer, their precedent block in condensed form:]
**[engineer name]:** [project], [engineer_architect] ([year]) — [what_to_study]

---

*Engineering Council — Session [session_id]*
````

#### Step 4c — Write the Markdown file

Write the assembled Markdown content to `engineering-council-review-<session_id>.md` in the user's current working directory. If the working directory is not writable, write to `~/Documents/engineering-council-review-<session_id>.md` instead.

#### Step 4d — Convert to PDF

Run the following command (adjust pandoc and wkhtmltopdf paths to match your installation):

```
pandoc "engineering-council-review-<session_id>.md" -o "engineering-council-review-<session_id>.pdf" --pdf-engine=wkhtmltopdf -V geometry:margin=2.5cm -V fontsize=11pt -V mainfont="Georgia"
```

If pandoc or wkhtmltopdf are not on PATH, use the full absolute path to each binary.

Run this command from the same directory as the `.md` file, so relative paths resolve correctly.

If the command succeeds: state the full path to the PDF.

If the command fails: state the error clearly and note the `.md` file is still available for manual conversion.

After completion, state:

> Engineering Council session complete. PDF saved to: [full path to PDF file]

---

## Section 5: Diagram Standards

All diagrams in this skill must meet the following standards:

### ASCII Technical Diagrams (structural, spatial, detail drawings)

Use for: structural cross-sections, connection details, plan details, material assemblies, load path diagrams.

Required elements:
- Title block: `DETAIL: [what it shows] / Scale: NTS or approximate / Engineer: [name]`
- Dimensional annotations: use `← xxx →` and `↑ xxx ↓` notation for key dimensions
- Material callouts: use abbreviations within or beside elements (RC C32, S355 steel, GLT timber, etc.)
- The specific engineering issue annotated inline: `ISSUE: [what is wrong here]`
- The required fix annotated inline: `FIX: [what should be here]`

Use box-drawing characters: `┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼` for structural elements. Use `▓` fill for solid concrete/masonry, `░` for lighter fill, `╱╲` for hatching, `─ ─` for dashed lines.

### Mermaid Diagrams (systems, flows, dependencies)

Use for: HVAC systems, load paths as flow diagrams, structural hierarchy, environmental performance flows, energy chains.

Required elements:
- Node labels include key technical values where relevant (temperatures, loads, flow rates)
- Problem nodes highlighted with `style NodeID fill:#ff6666` (red = issue)
- Missing element nodes: `style NodeID fill:#ffaa00,stroke-dasharray: 5 5` (orange dashed = absent)
- Good/compliant nodes: `style NodeID fill:#66bb66` (green = correct)
- Caption after the diagram: `*[what this diagram shows and what to fix]*`

### Precedent References

Format: named project + engineer or architect + year + specific principle demonstrated + what specifically to study in that project. Do NOT describe precedents generically — be specific about the drawing, detail, or system to look up. Precedents must be real projects that exist in published documentation.

---

## Section 6: Token Optimization

Each subagent prompt is composed of three layers: (1) static persona card content, (2) static phase template content, and (3) variable content — the normalized brief plus any prior-phase outputs. The static layers (1) and (2) become prompt-cache prefixes after the first subagent dispatch in a session — repeat dispatches on the same project reuse those cached prefixes. To preserve caching efficiency: never inline variable data into persona cards or phase templates. Always append variable content at the end of the subagent prompt, with the normalized brief as the final item.

---

## Section 7: Model Selection

| Phase | Model | Reason |
|-------|-------|--------|
| Phase 1: Parallel analysis (10×) | claude-sonnet-4-6 | Engineering reasoning + diagram generation requires full capability |
| Phase 2: Dependency mapping — council head | claude-haiku-4-5-20251001 | Structured pattern recognition across 10 JSONs; no design reasoning required |
| Phase 3: Synthesis — council head | claude-opus-4-7 | Full judgment across all phase data; highest reasoning requirement |

---

## Section 8: Output Usage

The PDF report is written to the user's current working directory as `engineering-council-review-<session_id>.pdf`. The intermediate Markdown file is also retained — feed it back to Claude with a targeted question for further interrogation: "Which chain in Phase 2 is most urgent for the structural system?" or "Expand Khan's connection detail into a full specification." or "Which precedent references should I study first for the material strategy?"

---

## Section 9: Swapping the Roster

**To replace an engineer:** Copy any existing persona card from `references/council/` (e.g., `01-structural-logician.md`). Edit the `id`, `name`, `field`, and `role` fields in the YAML frontmatter, rewrite all content sections to reflect the new engineer's philosophy and methodology, and save the file with a new filename. Remove the original card you are replacing. The controller reads all `.md` files with numeric prefixes in `references/council/` at runtime — any card present (other than `00-council-head.md`) is treated as a council member.

**To run a specialized council** (e.g., all sustainability-focused engineers, or a fabrication-focused panel): Remove standard cards and add specialized ones before invoking. The phase templates are persona-agnostic — they work with any engineer card that follows the standard frontmatter schema (`id`, `name`, `field`, `role`).

**To adjust council size:** The session can run with fewer than 10 engineers. Update dispatch loops in Phase 1 to match the active roster count. The dependency mapping and synthesis remain valid at any count.
