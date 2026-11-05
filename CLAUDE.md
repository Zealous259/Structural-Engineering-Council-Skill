# CLAUDE.md: engineering-council

## Plugin overview

An engineering review panel of ten engineers across five fields and a neutral chair, run as ONE subagent call. It reviews a design against the NCC and Australian Standards and returns a text report in the session: sealed lane analyses with rough numbers, up to three ASCII details, cross-field chains, a compliance list, a status and a fix order. No grades, no votes, no files.

## File structure

| File | What it controls |
|------|-----------------|
| `skills/engineering-council/SKILL.md` | The controller only: how the main session writes the brief, spawns the agent, fact-checks and relays |
| `agents/eng-council.md` | The council itself: ground rules, the five sections, the report template, the chair and the ten lane cards |
| `skills/engineering-council/README.md` | History, the audit of v1, and the measured token costs |

## Rules for agents working here

- Behaviour changes go in `agents/eng-council.md`. One lane card per engineer, one paragraph each. Keep lanes from overlapping: a problem belongs to one lane.
- `SKILL.md` stays small: everything it holds enters the main context on every run.
- The chair (Chen) never gives an engineering opinion and adds nothing the ten did not say.
- Lane cards are deliberately opinionated. Do not moderate their positions.
- No NCC clause numbers anywhere in the cards: cite the NCC by Section and topic. The 2022 edition renumbered the clauses, and v1's hard-coded numbers mixed editions.
- No em dashes or en dashes in any file here.
- The output has no score, grade or vote. Status is triage by rule, not a grade.
- After editing the agent file, restart Claude Code before testing: agent files load at startup.
- Keep what makes v2.1 cheap (tested 5 Nov 2026), and retest before removing any of it: `omitClaudeMd: true` in the agent frontmatter, the closing "Delivery" section (without it the agent wrote its report as plain text first in 5 of 8 runs), the three depth floors in ground rules 3 and 4 (without them low effort lost worked sums), `effort: "low"` in SKILL.md for runs with files only (a text brief at low effort did no thinking and lost its numbers), and `shrink.py` for images. Keep the main session out of the drawings until the fact check (SKILL steps 1 and 3): one session that measured them first sent a 648-word brief, and the council cost 85k instead of 60k to 65k.
