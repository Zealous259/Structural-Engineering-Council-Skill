# Engineering Council: history, audit and costs

## Versions

- **v1 (Aug 2026).** Twelve subagents in three phases: ten engineers in parallel (one per persona card, JSON out), a facilitator mapping dependency chains, a facilitator synthesis, then a Markdown report converted to PDF with pandoc and wkhtmltopdf. 130 KB of instructions across 15 files.
- **v2 (Nov 2026).** One Read-only custom agent (`eng-council`) holds the whole council in its system prompt; this skill is only the controller. Two turns: read every file at once, then write the report. Text in the session, no files. 25 KB across two files.
- **v2.1 and v2.1.1 (5 Nov 2026).** The same council for about 60k to 65k agent tokens with five drawings, where v2 took 103k to 113k. v2.1.1 only changes when the main session opens the drawings: see below.

## Audit of v1 (5 Nov 2026)

Tags: **verified** = read, run or measured in the audit session; **inferred** = reasoned from what was read.

**Would it still work?** No.

1. **Model names.** It hard-codes `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` and `claude-opus-4-7`. The Agent tool now takes only the aliases `sonnet`, `opus`, `haiku`, and those three are a generation old (verified against the tool schema).
2. **The PDF step.** It needs pandoc and wkhtmltopdf installed. Even with them, `-V geometry` and `-V mainfont` are LaTeX settings the wkhtmltopdf engine ignores, and pandoc prints Mermaid blocks as raw code without a filter, so the eleven Mermaid diagrams would have printed as code (inferred).
3. **JSON as the transport.** Every ASCII drawing had to travel inside a JSON string with `\n` escapes. One backslash in a hatch pattern breaks the parse, which is why the skill needed a re-dispatch rule (inferred).
4. **The caching claim was wrong.** Each Phase 1 prompt began with a different persona card, so the ten prompts shared no cacheable prefix, and caches expire in minutes, not across sessions. Worse, the controller had to write every card and template into twelve prompts as output, roughly 150 KB of output tokens per run, which no cache covers (inferred from the file sizes).
5. **Models in the wrong places.** The dependency chains, the most cross-disciplinary reasoning in the pipeline, went to Haiku; the synthesis, which only restates, went to Opus (inferred).
6. **Contradictions inside the skill** (verified): Phase 0 asks for "all 6 elements" of a brief that lists 7; Section 9 says the controller reads every numbered card at runtime while Phase 1 hard-codes ten paths.
7. **NCC references that cannot all be right.** Carrier's card says Section J Part J6 is air-conditioning and ventilation; Fuller's and Sobek's say J6 is artificial lighting (verified). The cards mix the pre-2022 clause format (J3.4, B1.4, F4.6) with 2022 part numbers, and the 2022 edition renumbered every clause (inferred). Brunel lists AS 4600 and AS/NZS 4600 as two standards (verified), Khan's "AS/NZS 1170.4" is AS 1170.4, and Rice's card gives AS 1214 the title of the galvanizing standard, AS/NZS 4680 (inferred). And Phase 1 required every engineer to cite a specific clause, which turns memory errors into a "Compliance Register".
8. **No timber.** AS 1720.1 appears nowhere, and timber barely appears in the cards (verified). Fire, egress, acoustics and access were all in one card.
9. **The engineers never saw the drawings.** The controller described each image in text and the engineers critiqued the description (verified, Section 2).
10. **Built-in duplication.** Five of the ten (Khan, Maillart, Fuller, Sobek, Otto) share "minimum material" as their core, and the rule "do not simulate the other engineers" in isolated agents guaranteed they would repeat each other (inferred).
11. **Cost.** With twelve subagent spawns at about 67k tokens each before their prompts, v1 would have started near 0.8M tokens a run (inferred).

## What v2 keeps and what it changes

**Kept:** the ten engineers and Chen; each engineer's conviction, review lens and positions, compressed into a lane card; severity (CRITICAL, MAJOR, MINOR); problems, missing elements and fixes; drawings and precedents; dependency chains that must state their mechanism, systemic gaps and the facilitator's neutrality; the compliance statuses (NON-COMPLIANT, VERIFY, ADVISORY); the three statuses with v1's thresholds; a fix order with timing; no grades and no votes.

**Changed:** one Read-only custom agent and two turns; lanes, so each problem has one owner instead of five; the agent reads the drawings itself; `[seen]`, `[brief]` and `[assumed]` tags on every claim; rough numbers with their working; the NCC cited by Section and topic, never by clause number; AS 1720.1 and timber added across three lanes; ASCII only, because it renders in a terminal; guest engineers for one-off specialists; a follow-up mode; the main session fact-checks before relaying; no confirmation stop unless the structure is unclear.

**Removed:** the biographies (about 40% of each card), the vocabulary lists, the JSON schema, the PDF pipeline and Mermaid.

## Measured cost (5 Nov 2026)

Headless runs (`claude -p`, hooks off, the main session on Opus 5.5 at its default effort) on the same project notes and the same five drawings of one test building: a section, a roof plan and three details. Dollar figures are the run's own `costUSD` at API rates, a proxy for subscription usage.

| | arch-council-lite | v2 first build | v2, `effort: medium` | **v2 final** |
|---|---|---|---|---|
| Council agent turns | 1 | 3 | 3 | **2** |
| Agent fresh input (tokens) | 61.0k | 138.5k | 128.5k | **45.7k** |
| Agent output, thinking included | 1.7k | 56.6k | 54.3k | **54.1k** |
| Agent cost | $0.17 | $0.91 | $0.87 | **$0.66** |
| Main session cost | $1.66 | $1.78 | $1.72 | **$1.38** |
| **Whole run** | **$1.83** | $2.70 | $2.58 | **$2.04** |
| All input processed, main and agent | 375.5k | 714.6k | 480.5k | **282.5k** |
| Report as relayed | 933 words | 3,922 words | 3,974 words | 3,642 words |

What the numbers say:

- **A whole run costs about what a lite run costs** (+12%), while processing a quarter fewer input tokens. The agent's own input is a quarter lower than the lite's general-purpose agent (45.7k against 61.0k), because a Read-only custom agent starts at about 16k of context against about 67k.
- **The difference is thinking.** The council plans ten lanes and works its rough numbers in about 50k tokens of thinking before a 3,000-word report. `effort: medium` barely moved it (minus 6%), because the agent already ran at medium: its transcripts record medium with or without the parameter. Opus is no cure (see the tests below).
- **The first build wrote its report twice**: as a message, then again inside the hand-back call, a third turn that re-read the whole context. Ground rule 2 now puts the report straight into the hand-back; that removed a third of the agent's cost.
- **The main session is most of any council's cost**, lite included: it reads the drawings, writes the brief and fact-checks. Its fact-check paid for itself in every run. It caught a height that was wrong in the brief, two misread views, a mis-tagged claim and one wrong sum.
- **v1 was not run.** The audit's estimate (point 11) puts it near 0.8M tokens a run, against about 46k fresh input for this agent.

Quality on that test (a keyword check against 16 findings, 8 named before any run and 8 added after reading the first report, then each report read in full): the first build hit 14 and the final build 15. The one it missed, a height that was wrong in the brief, the main session's fact check caught.

## Tests of what the first round left open (5 Nov 2026, morning)

Headless again, hooks off. The plugin was loaded from a copy without its `agents/` folder, and the agent was passed in with `--agents` as plain `eng-council`, the name a user-level install shows; nothing under `~/.claude` was touched. Costs are each run's `costUSD` at API rates.

| Run | What it tested | Result | Cost |
|---|---|---|---|
| L1 | "Run the engineering council on...", no skill named; the plain agent name | The skill triggered and called `eng-council`; two agent turns, report written once; 13 of 14 topic checks, as the overnight final | $2.10 (agent $0.57) |
| L3 | The fallback: agent file added after the session had started | One general-purpose Sonnet agent with the file as its prompt; same quality; first agent turn 67.1k tokens against 21.6k | $2.70 (agent $0.74) |
| L6 | Another building (a house), PDFs only, a guest engineer | The main session named pages, the council read the PDF pages itself, and the guest got a section | $3.05 (main $2.40, reading 36 PDF pages) |
| L2, L2b | A bare idea, nothing drawn | Ran the whole council anyway, twice: "run it" beat "ask one question first" | $1.11, $1.64 |
| L2c | The same, after the ask rule was tightened | Asked one question and stopped | $0.56 |
| L4 | A deep run with `model: "opus"` | Thought to the 128k output limit with no report; stopped after 27 minutes | about $4.20 recorded |
| L5 | A follow-up: Khan and Rice on one connection | One call, two lanes, carrying the fact check's corrections | $1.62 |
| L5b, L7, L5c | The follow-up again, after three different wordings of the write-once rule | Wrote its answer as text, then repeated it in the hand-back each time | about $0.20 extra per follow-up |
| L6b | The precedent rule after the fix, on L6's brief | One real precedent, and "look for" guidance where unsure | $1.55 |
| L1b, L7 | The final agent text, full report | Two turns, written once (7 of 7 full reports across the morning) | $1.25; $2.20 for L7's pair |

**Changed after these runs:** the ask rule (SKILL step 1); deep mode removed (step 2); a follow-up carries the fact check's corrections (step 4); ground rule 2 no longer counts turns; precedents are "up to three", and none is better than a guess.

**Known limits:**
- **Status varies at the CRITICAL boundary.** On the same brief, three runs said REQUIRES REDESIGN and one NEEDS SIGNIFICANT REWORK. The main CRITICAL and the fix order were the same in all four.
- **Reports run long:** 3,300 to 3,600 words against the 2,000 to 2,800 target.
- **Drawings run slightly wide:** they sometimes go one to four characters past the 76 limit (77 to 80).
- **A follow-up writes its answer twice** (4 of 4); a full report does not (7 of 7). Fixed in v2.1 by the closing Delivery section: 2 of 2 follow-ups were written once.
- **One invented precedent, caught.** Before the precedent fix, one report in six named an invented precedent, and the fact check caught it.

**Install paths:** `claude plugin install` from a local marketplace into an isolated `CLAUDE_CONFIG_DIR` installs the plugin (2.0.0 at the time) with the agent, and `claude plugin validate` passes. Two stale v1 `plugin.json.bak-*` files were shipping inside `.claude-plugin/`; they are removed.

## v2.1 and v2.1.1: about 60k to 65k tokens a run (5 Nov 2026, afternoon and evening)

The target was the architectural council's figure, which counts the council agent alone: its input, cache reads and writes included, plus its output (`council_cost.py` counts it that way). The main session is not in these numbers. The test was the same brief with the same five drawings each time, sent straight to the agent.

| Version | Agent tokens | Thinking | Problems found (of 14) | Worked sums | Evidence tags | Chains | Compliance rows |
|---|---|---|---|---|---|---|---|
| v2.0, 4 runs | 102.6k to 112.8k | 26.1k to 36.4k | 11 to 13 | 6 to 12 | 24 to 48 | 3 to 4 | 11 to 16 |
| Low effort alone, 2 runs | 57.2k, 61.0k | 10.7k, 14.5k | 11, 10 | 4, 3 | 14, 29 | 3, 4 | 12, 13 |
| **v2.1: low effort plus depth floors, 2 runs** | **60.2k, 61.3k** | 13.1k, 14.4k | **11, 13** | 6, 5 | 33, 46 | 4, 4 | 12, 12 |
| Normal effort with the other savings, 1 run | 68.5k | 24.0k | 12 | 7 | 22 | 4 | 12 |
| v2.1 installed, the session's own 648-word brief, 1 run | 84.8k | 37.8k | 14 | 8 | 41 | 3 | 13 |
| v2.1, that brief sent straight to the agent, 1 run | 73.2k | 24.8k | 14 | 6 | 33 | 4 | 13 |
| **v2.1.1 on a real install, the session's own 374-word brief, 1 run** | **65.0k** | 17.4k | **12** | 4 | 48 | 4 | 14 |

Every run wrote three drawings and covered all ten engineers, and every run except one v2.0 run gave the same status.

**The brief sets the cost.** The 60k runs used a fixed 420-word test brief. After the install, a run on a real install let the session write its own brief. It read the five drawings first, because the Files line in step 1 says to read the originals. It measured the section with two scripts and sent 648 words with a guest engineer, where step 1 asks for about 300. The council thought for 37.8k and cost 84.8k. Sent straight to the agent again, the same brief cost 73.2k with 24.8k of thinking, so the richer brief, not chance, is the likely cause (inferred, two runs each). Both runs found 14 of 14, but the 14th was already in the brief.
- **Order:** v2.0's live run read the drawings after the council, for the fact check, and sent 452 words.
- **Cost in dollars:** at API rates the live council cost $0.53, against $0.49 for v2.0's live run and $0.23 to $0.29 for the 60k runs. Its saving is in context, which is cheap; its extra is in thinking, which is not.
- **The whole session:** it cost $2.49 against $1.91, and $1.96 of that was the main session.

**v2.1.1 moves the drawing read to the fact check** (5 Nov, evening). Step 1 now says to write the brief from the request and not to open or measure the drawings. Step 3 opens the originals for the fact check, as v2.0 did. The retest used a real install with hooks on and the same request, with the skill loaded from a copy of the plugin (one run):
- **Order:** the session ran `shrink.py`, called the council, then opened the five originals. The brief was 374 words, with no guest engineer (the v2.1 live session had added one, so that may account for part of the gap).
- **The council:** 65.0k tokens with 17.4k of thinking, where the v2.1 live run took 84.8k and 37.8k. It found 12 of the 14 problems. It gave 4 worked sums, the fewest of any v2.1 run (5 to 8).
- **The fact check caught both misses**, and more: in all it listed 12 numbered corrections and three points the council had not raised, and none changed the status.
- **Dollars at API rates:** the council cost $0.34 and the whole session $2.14. v2.1's live run cost $0.53 and $2.49, and v2.0's $0.49 and $1.91. The other $1.80 is the main session, mostly the fact check and the verbatim relay.

**The same brief with no drawings** (v2.1 agent, one run each):
- **Low effort:** the council did no thinking at all. 15.4k tokens, 2,060 words, 2 worked sums and two drawings. Only 8 of its 24 CRITICAL and MAJOR lines carried a number.
- **Default effort:** 25.6k tokens, with 7.1k of thinking, 3,432 words, 5 worked sums and three drawings. 22 of its 37 lines carried a number, the same share as the drawing runs.

Both found 9 of the 14 problems, and at least two of the 14 can only be seen in the drawings. So SKILL.md passes `effort: "low"` only when the council reads files.

**What changed, and what each change saved:**

- **`omitClaudeMd: true`:** the agent no longer receives the user's `CLAUDE.md` files and memory index, which it read on both of its turns. It now starts with about 11k tokens: the council, the harness, its tool and the brief.
- **`shrink.py`:** the council gets copies of the drawings at 1,400 px at most. Five 2,000 px drawings fell from 22.8k to 14.8k tokens, and the labels stayed legible.
- **`effort: "low"` when the council reads files:** thinking roughly halves, from 26k to 36k down to 11k to 15k. A text brief keeps the default effort (above).
- **Three depth floors** (ground rules 3 and 4):
  - every CRITICAL and MAJOR that a number can settle carries one;
  - every bullet line ends with its evidence tag;
  - every number in the brief is checked against the drawings.

  Low effort alone lost worked sums and tags; the floors brought them back for about 1.5k tokens a run.
- **A closing "Delivery" section.** With `omitClaudeMd` and no closing section, the agent wrote its report as plain text first in 5 of 8 runs, with or without the architectural council's opening hand-back line. Then either the harness forced a full rewrite (114k to 157k a run) or the agent handed back "See report above.", which delivers nothing. Every run with the closing section wrote its answer once: 9 of 9, seven full reports and two follow-ups.

**Follow-ups.** The test question was the morning's Khan and Rice question, with three drawings at 2,000 px (one run each). v2.0 wrote every follow-up twice (4 of 4; the two scored runs cost 88.7k and 137.3k). v2.1 wrote it once both times.
- **At low effort,** which the step 2 rule gives a follow-up with files, it cost 70.4k and had 16 worked sums.
- **At the default effort** it thought for 55k and cost 102.6k, with 8 worked sums.

With `shrink.py`'s copies it would cost about 5k less (inferred from the per-image cost). A follow-up that works a connection through costs about as much as a full run.

**What did not change:** the main session still reads the original drawings and fact-checks. The council's most frequent miss on this brief is a height the brief gives wrong and the section draws correctly. The new rule to check the brief's numbers against the drawings did not fix that (missed in both v2.1 runs, caught in the normal-effort run). Catching it is the fact check's job, and it caught it.
