# Engineering Council

An engineering review council for Claude Code in one agent call. Ten engineers, each owning one lane, and a neutral chair review a building, structure, detail or services scheme against the NCC (Australia's National Construction Code) and Australian Standards. The report comes back as text in the session: what is wrong, what is missing, what must change, and in what order.

**No grades. No votes. No files.**

## How it works

**One run.** Your session writes a short brief from your request and what it already knows, without opening the drawings, and makes a single call to a Read-only agent that sees the brief and nothing else from the session. `shrink.py` hands the agent copies of the drawings at most 1,400 px on the long side. The agent reads every listed file in its first turn and writes the whole report into its hand-back in its second. Your session then opens the original drawings, checks the claims the status rests on, and relays the report unchanged with a Fact check list under it.

**Inside the council.** Each engineer writes as if the other nine did not exist and leads with the most damaging point in their own lane: located on the drawings, graded CRITICAL, MAJOR or MINOR, every claim tagged by its evidence, with a rough number wherever a number settles the argument. Up to three ASCII details show the worst issues with `ISSUE` and `FIX` callouts. The chair, Dr. Sarah Chen, maps chains where one lane's problem forces another's, names gaps no one raised and leaves clashes open. Then she writes the synthesis: a status set by rule, a fix order, up to three precedents and the limits of the review. She adds no engineering opinion.

## Council

| Engineer | Lane | Known for |
|----------|------|-----------|
| Fazlur Rahman Khan | Structural system: load path, lateral stability, grid | The tube system, Willis Tower, John Hancock Center |
| Cecil Balmond | Structural geometry: is the shape doing the work | Arup's Advanced Geometry Unit, "Informal" |
| Isambard Kingdom Brunel | Buildability: sequence, temporary works, safe design | Great Western Railway, Clifton Suspension Bridge |
| Robert Maillart | Material efficiency and concrete durability | Salginatobel Bridge |
| R. Buckminster Fuller | Whole-system energy, water and material loops | Geodesic dome |
| Werner Sobek | Envelope performance and embodied carbon | ILEK Stuttgart, Triple Zero |
| Willis Carrier | Moisture, condensation, ventilation and plant | The psychrometric chart |
| Ove Arup | Integration seams, fire, egress, access, acoustics | Total design |
| Peter Rice | Connections and material character | Pompidou gerberettes, Menil Collection roof |
| Frei Otto | Lightweight structures and roofs | Munich Olympic roofs, Mannheim gridshell |

**Chair:** Dr. Sarah Chen, a neutral facilitator who maps cross-field chains and holds no engineering opinions.

## What you get

1. **Engineers:** ten sealed analyses, most damaging point first, each finding located and tagged `[seen]`, `[brief]` or `[assumed]`, with rough numbers where a number settles the argument.
2. **Drawings:** up to three ASCII details of the most critical issues, with `ISSUE` and `FIX` callouts.
3. **Chains:** where one engineer's problem causes another's, plus systemic gaps and clashes between fixes.
4. **Compliance to check:** NCC Sections and Australian Standards, each NON-COMPLIANT, VERIFY or ADVISORY.
5. **Synthesis:** a status by rule (READY FOR ITERATION, NEEDS SIGNIFICANT REWORK, REQUIRES REDESIGN), a fix order, precedents and the limits of the review.

## Measured cost and quality

**Tokens per run**, counted the way the architectural council counts its board: the council agent's input, cache writes, cache reads and output. The main session is not in these numbers. Every run is a headless test on the same project with five drawings (5 Nov 2026).

- **v2.0 took 102.6k to 112.8k a run.** v2.1 takes about 60k. The agent starts without the user's CLAUDE.md and memory index (`omitClaudeMd: true`), and when it reads files it runs at low effort, with three depth floors that keep its worked numbers. It also reads 1,400 px copies of the drawings.
- **A report written twice doubles the cost.** The first v2 build wrote the report as a message and again in its hand-back (217.6k). With `omitClaudeMd` and no closing Delivery section, 5 of 8 runs wrote it as text first, and a forced rewrite cost 114k to 157k. The Delivery section stopped it (9 of 9).
- **The brief sets the thinking.** A session that measured the drawings before writing the brief sent 648 words, and the council cost 84.8k. v2.1.1 writes the brief first: 65.0k.
- **A text brief** costs 25.6k at the default effort. Low effort is used only with files: on a text brief it skipped the thinking, and most findings lost their numbers.

**Problems found.** The test project has 14 known problems across structure, envelope, compliance and drainage, and each report is checked for them by keyword. v2.0 found 11 to 13. v2.1 found 11 and 13 at about 60k. v2.1.1 found 12, and the session's fact check caught the other two. Without drawings the council found 9: at least two of the 14 can only be seen in them.

## Install

By hand: copy `agents/eng-council.md` to `~/.claude/agents/` and the folder `skills/engineering-council/` to `~/.claude/skills/`, then start a new Claude Code session (agent files load at startup).

As a plugin: this folder is a plugin root (`.claude-plugin/plugin.json`). Put it in a local plugin marketplace, install `engineering-council` from there and restart Claude Code. The agent may then be listed as `engineering-council:eng-council`; the skill uses whichever name the agent list shows.

`shrink.py` needs Python 3 with Pillow (`pip install pillow`) to make the smaller drawing copies. Without Pillow the council reads the original drawings, which cost more: five 2,000 px drawings took 22.8k tokens against 14.8k.

Then say "engineering council" with a design, drawings or a model capture.

## Customising

Edit a lane card in `agents/eng-council.md` (one paragraph each). For a one-off specialist (a fire engineer, an acoustician, a geotechnical engineer, your tutor), add a guest engineer line to the brief.

## Files

| File | Role |
|---|---|
| `skills/engineering-council/SKILL.md` | The controller: how the main session writes the brief, runs the council, checks and relays |
| `agents/eng-council.md` | The council: ground rules, the five sections, the report template, the chair and the ten lane cards |
| `skills/engineering-council/shrink.py` | Makes the 1,400 px drawing copies the council reads |
| `skills/engineering-council/README.md` | The audit of v1, the measured costs and every test |

## Security

- The council's only tool is Read, and it is told to read only the files the brief lists (an instruction: Read itself can open any file you can). It cannot write files, run commands or reach the network.
- It starts without the user's CLAUDE.md files (`omitClaudeMd: true`), so personal instructions and memory stay out of its context.
- The skill runs one local command in the main session, `python shrink.py <paths>`. It reads the drawings it is given and writes resized copies into a new private folder with a random name under the system temp folder (`tempfile.mkdtemp`). It never changes the originals and makes no network calls.

## Version

v2.1.1, November 2026. It replaces v1, which ran twelve subagents in three phases, passed JSON between them and exported a PDF through pandoc and wkhtmltopdf. The audit behind the change and every measured run are in `skills/engineering-council/README.md`.
