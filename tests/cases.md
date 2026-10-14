# Test cases

Each case is run twice against a real project directory: once with the skill
(`/deepen-prompt <task>`), once as a control given only the original
four-question prompt with the same read access. Controls must be told not to
read this repo or `~/.claude/skills` — in testing, an unrestricted control
found and read the skill on its own.

Score each reply with the mechanical checks, then compare by hand on the
questions the script can't answer (below).

```bash
python3 skills/deepen-prompt/scripts/check_reply.py reply.md /path/to/project
```

## Baseline cases (no workspace — shaped v1)

| ID | Task | Observed failure without the skill |
|---|---|---|
| B1 | "Write a function that deduplicates customer records in our CRM export." | Rewrote into "an auditable entity-resolution pipeline … not a one-off dedup function"; 300 hand-labelled pairs + κ for verification; ~450-word rewrite. |
| B2 | "Write a market sizing for solar mini-grids in Nigeria for my pitch deck." | One slide → GIS + OnSSET + HOMER + Monte Carlo + DCF project; only long-horizon checks. |
| B3 | "Help me figure out why our React app feels slow." | 7-step program, 5 attachments, 5 brackets; ~20 tools unranked. |
| B4 | "Make this prompt deeper, not bigger: 'Summarize the latest research on intermittent fasting for my newsletter.'" (no four questions) | Stayed small but shallow: still summarise-from-memory, no raw source, no outside check. |

## Real-workspace cases

| ID | Project | Task | What a good reply does |
|---|---|---|---|
| T1 | llm-council (FastAPI 3-stage LLM council) | "Make the chairman's final answer better." | Keeps the deliverable (the Stage 3 prompt); reads a saved run and finds a concrete chairman failure; notices model names leak into Stage 3; oracle = keyed questions where Stage 3 must be right whenever any Stage 1 answer was, shown failing on current outputs. |
| T2 | private: AI voice-receptionist startup (Nigeria) | "Figure out how to price <product> for the pilot." | Prices only the blanks in the pilot offer (tiers wait for pilot data, per the startup's own plan); floor = measured cost-to-serve at a weaker ₦/$; ceiling = audited loss; oracle = model reconciles to vendor bills + signatures/fees received. |
| T3 | private: pre-launch B2B company | "Write a LinkedIn post announcing <company>." | Keeps one post; every claim traced to the company's claims register; notices its own playbook and launch blockers; oracle = claim-trace table seen failing on a planted unsupported claim + cold read by target readers. |

## Judged by hand

1. Is the deliverable the user's (or its smallest correct form)?
2. Does the **Found** line cite something that is actually in the file it names?
3. Would the first item of move 1 change the result on its own?
4. Is the "Done when" check one the executor could not quietly pass without doing the work?
