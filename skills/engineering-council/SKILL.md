---
name: engineering-council
description: The Engineering Council in one subagent pass. Ten engineers (Khan structure, Balmond geometry, Brunel buildability, Maillart concrete, Fuller systems, Sobek envelope and carbon, Carrier moisture and plant, Arup integration fire and egress, Rice connections, Otto lightweight roofs) chaired by Chen review a building, structure, detail or services scheme against the NCC and Australian Standards. Sealed lane analyses with rough numbers, up to three ASCII details, cross-field chains, a compliance list, a status and a fix order. Text in the session; no files, no PDF. Use for "engineering council", "eng council", "tech council", "present it to the engineers", or any technical crit of structure, envelope, services, fire or buildability. About 26k tokens for a text brief, 60k to 65k with five drawings (measured).
---

# Engineering Council (v2.1.1, Nov 2026)

The council lives in the agent `eng-council`, whose file is `~/.claude/agents/eng-council.md` (in a plugin install, `agents/eng-council.md` at the plugin root, two folders above this skill). Its system prompt holds the rules, the report template and the ten lane cards, so almost nothing enters the main context. Do not read the agent file unless the fallback in step 2 needs it.

## 1. Write the brief

One block, at most about 300 words. Neutral: state the weak and unfinished parts too, never sell the work. Write it from the request and what the session already knows. Do not open or measure the drawings for it: the council reads them, and you read the originals at the fact check (step 3). On 5 Nov 2026 a session that measured the drawings first wrote 648 words, and the council's thinking roughly doubled.

- **What and stage:** building or element type, course or client, design stage (concept, developed, documentation), and what the review is for (a tutor's or visiting engineer's stated focus).
- **Site and climate:** city, NCC climate zone, exposure (wind region, terrain, coast), ground conditions if known, and which way the main faces point in compass terms.
- **Program and occupancy:** uses, numbers of people, the BCA class if one has been decided (the council checks it).
- **Structure:** system, materials, spans, grid, member sizes, lateral system, foundations. Say what is decided and what is still open.
- **Envelope:** roof, wall and floor build-ups, glazing and panels, membranes, R-values.
- **Services:** HVAC, hydraulics, electrical, fire; plant sizes and where the plant sits.
- **Constraints and assessment:** the NCC edition and sections the course names, budget, fabrication method, deadline.
- **Numbers:** each one says what it measures and where.
- **Not shown:** what is not designed or not visible, so the council does not invent it.
- **Files:** absolute paths, at most 8: sections, details, plans, model captures, schedules. Run the image paths through `shrink.py` in this skill's folder (`python shrink.py <paths>`) and list what it prints: copies at most 1,400 px on the long side, in a temporary folder. Labels stay legible and the council's image cost falls by a third. For a drawing set PDF, name the pages to read (sections and details first). A live Rhino or Revit model goes as captured views: the council reads images, never a .3dm or .rvt.
- **Guest engineers** (optional): a fire engineer, acoustician, facade or geotechnical engineer, or the review's visiting engineer, one line each.

Ask first in one case only: nothing is drawn (no drawing, model capture or sketch) and the structural system is not stated. Then ask one question, for the structural system or a sketch, and stop, even when the request says to run the council now: on a bare idea a full run returns mostly `[assumed]` text. If the user answers, or says to run it anyway, run it on what there is. In every other case do not wait for confirmation: the report opens with the brief.

## 2. Run it

One Agent call: `subagent_type: "eng-council"` (a plugin install may list it as `engineering-council:eng-council`; use the name the agent list shows), `description: "Engineering council"`, prompt = the brief block and nothing else. Effort: pass `effort: "low"` when the prompt lists files, and leave effort out when it lists none. Measured on 5 Nov 2026: with five drawings, low effort matched the full-effort scores on half the thinking (about 60k a run against 106k); on a text brief, low effort did no thinking and most findings lost their numbers, while the default kept them for 26k. No opinion of yours and none of the session's history: the council stays independent of whoever built the work. Never raise the model or the effort for a deeper review: on Opus it thought past the 128k output limit without writing a report. Depth comes from a follow-up round (step 4).

Fallback when no such agent type is listed (installed during this session, before a restart, or missing): Read the agent file and spawn ONE `general-purpose` agent with `model: "sonnet"` and the same effort rule, prompt = the file's body below the frontmatter, then the brief. Same report, but about 45k more tokens of spawn overhead (measured).

## 3. Check, then relay

1. Fact-check every claim about the design that the status or the fix order leans on, against the original files (not the `shrink.py` copies) or the model: open the drawings now, after the council, not before it. A council reading a drawing can misread a label or a level. Do not edit the report: add a short **Fact check** list under it for anything wrong.
2. Relay the report verbatim, as text in the session. No file, no PDF.
3. Tag per the working protocol if CLAUDE.md defines one, once and not per line: the report is agent output, so every standard, NCC reference, rough number and precedent in it is unverified until checked against the edition and the standard itself.

## 4. Follow-ups

A second round, depth on one engineer, or one issue worked through: one more `eng-council` call (effort by the rule in step 2, so a follow-up without files runs at the default) with the brief, the parts of the previous report the question concerns, every correction from your fact check, and the specific question. Never rerun all ten unless asked.

## Changing the council

Edit a lane card in the agent file (one paragraph each). For a one-off specialist, pass a guest engineer in the brief. History, the measured costs and the audit of v1: `README.md` in this folder.
