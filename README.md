# Engineering Council

Multi-disciplinary engineering review panel for architecture and engineering projects. 10 engineers across 5 fields analyze any design through distinct technical lenses and produce structured feedback with annotated technical drawings.

**No grades. No votes. Only: what is wrong, what is missing, and how to fix it.**

---

## Council Members

| Engineer | Field | Known For |
|----------|-------|-----------|
| Fazlur Rahman Khan | Structural Engineering | Tube structural system, Sears Tower, John Hancock Center |
| Cecil Balmond | Structural Engineering | CCTV HQ, Serpentine Pavilions, informal geometry |
| Isambard Kingdom Brunel | Civil / Infrastructure | GWR, SS Great Britain, Clifton Suspension Bridge |
| Robert Maillart | Civil / Concrete | Salginatobel Bridge, hollow-box concrete, thrust-line arches |
| R. Buckminster Fuller | Environmental / Systems | Geodesic dome, tensegrity, ephemeralization |
| Werner Sobek | Environmental / Sustainable | Triple-zero buildings, R128, ILEK Stuttgart |
| Willis Carrier | Building Services / Mechanical | Air conditioning, psychrometric chart, natatorium design |
| Ove Arup | Building Services / Integration | Sydney Opera House, Pompidou, total design philosophy |
| Peter Rice | Materials / Fabrication | Pompidou gerberettes, Menil Collection roof, An Engineer Imagines |
| Frei Otto | Materials / Lightweight | Munich Olympic roof, minimal surfaces, form-finding |

**Facilitator:** Dr. Sarah Chen (neutral, no engineering opinions — maps cross-field dependencies only)

---

## What It Does

1. **Normalizes your brief** — structures any input (text, image, 3D reference, drawing) into a standardized engineering brief and confirms with you before proceeding.

2. **10 parallel engineering analyses** — each engineer produces, through their specific technical lens:
   - A 200-300 word technical review (what is wrong, what is missing, how to fix it)
   - Specific problems with severity ratings (critical / major / minor)
   - Concrete improvement actions
   - A technical diagram specific to their primary concern (ASCII detail drawing OR Mermaid system diagram)
   - A real precedent reference with what specifically to study

3. **Cross-field dependency mapping** — Dr. Sarah Chen identifies where one engineer's concern directly causes or amplifies another's. These are presented as **concern chains**: "Khan flags X → which forces Carrier into Y → which Arup cannot resolve without Z." Each chain is rated critical/major/minor by its worst link.

4. **Priority synthesis** — a full feedback report: critical issues, major issues, minor issues, and an ordered improvement roadmap.

5. **PDF report** — all phases assembled into a formatted PDF in your working directory.

---

## Output

- No grade. No score. No verdict.
- **Status** (objective process marker only): READY FOR ITERATION / NEEDS SIGNIFICANT REWORK / REQUIRES REDESIGN
- All 10 engineer diagrams embedded in the PDF
- Cross-field dependency diagram in Mermaid
- All 10 precedent references indexed at the end of the report
- Improvement roadmap ordered: immediate → before-next-stage → before-construction

---

## Input Types

| Input | How it's handled |
|-------|-----------------|
| Text description | Normalized to brief |
| Image (photo, screenshot, render) | Described visually, engineers annotate with positional references |
| Plan / section / detail drawing | Described with legible geometry and dimensions, engineers produce parallel drawings showing problems |
| 3D file reference (Rhino, Revit, etc.) | Noted in brief; engineers produce abstracted 2D diagrams from description |
| Combination | All of the above, combined into one brief |

---

## Diagram Types

| Engineer | Typical Diagram Type |
|----------|---------------------|
| Khan (Structural) | ASCII load path / column grid plan with annotations |
| Balmond (Structural) | ASCII structural geometry sketch or Mermaid structural hierarchy |
| Brunel (Civil) | ASCII construction sequence diagram or cross-section |
| Maillart (Civil/Concrete) | ASCII concrete section with thrust line overlay |
| Fuller (Environmental) | Mermaid energy/material flow system diagram |
| Sobek (Environmental) | ASCII envelope cross-section with U-values or Mermaid energy chain |
| Carrier (Building Services) | Mermaid psychrometric / HVAC system diagram |
| Arup (Integration) | Mermaid coordination diagram showing discipline clashes |
| Rice (Materials) | ASCII connection detail with force annotations |
| Otto (Lightweight) | ASCII membrane or tensile structure with anchor forces |

---

## Prerequisites

- Pandoc installed at `C:\Users\balaz\AppData\Local\Pandoc\pandoc.exe`
- wkhtmltopdf installed at `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`

---

## Customizing the Roster

Replace any engineer card in `skills/engineering-council/references/council/` with a card following the same frontmatter schema (`id`, `name`, `field`, `role`). The controller reads all numeric-prefixed `.md` files in that directory. See SKILL.md Section 9 for full instructions.
