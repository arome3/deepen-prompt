# deepen-prompt

**Make any task deeper, not bigger.** A skill for
[Claude Code](https://claude.com/claude-code) (and any harness that reads the
[Agent Skills](https://agentskills.io/specification) format) that answers four
questions about your task, then rewrites your prompt to ask for exactly that:

1. What would a top professional in this field do here that you aren't asking for?
2. What is the rawest material they would start from, instead of what's already been digested?
3. Which specific methods and tools would they use?
4. What, other than you or the AI, would show the result is right?

The questions come from Felix Rieseberg's
[*How to be more ambitious: A tutorial for humans with models*](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/)
(Oct 2026). This skill is an independent implementation, not affiliated with
the author.

```
/deepen-prompt Make the chairman's final answer better.
```

---

## Why a skill, not just the prompt

Pasting the four questions works, but there's a catch. Tested without this
skill, agents answered all four questions with real domain depth, then:

- **made the task bigger instead of deeper.** "Write a dedup function" became
  "build an auditable entity-resolution pipeline". "One market slide" became a
  GIS modelling project. "Improve the chairman prompt" became a 60-question
  eval program with a harness, cached dataset and six variants;
- **listed instead of choosing:** 6–8 unranked items per question;
- **sized checks out of proportion:** 300 hand-labelled pairs and Cohen's κ
  for a CSV cleanup;
- **left blanks for you** (`[fill in X]`) for facts sitting in the repo;
- **wrote 300–450-word prompts** for 10–15-word asks.

Knowledge was never the gap. **Selection, proportion, grounding, and shape**
were. The skill adds:

| Mechanism | What it fixes |
|---|---|
| **Scope rule:** enlargement = anything not needed for correctness or for the outside check. If correctness needs a different form, use the smallest correct form. | Deeper → bigger drift, without blocking necessary reshaping (e.g. an expand/contract migration) |
| **Ground first:** read the project's own rules/plans and one actual instance of the raw data; report one concrete **Found** fact | Generic advice; `[brackets]` for findable facts |
| **Select and rank:** 1–3 items per question, most decisive first, one line each | Laundry lists |
| **Rawness ladder + access tags:** `found: path` · `you have it` · `→ next rung` | Naming sources you can't reach |
| **Oracle chosen by the named likely failure,** fixed before work starts, *shown failing once* | "Have an expert/another AI review it"; checks that can't fail |
| **Five-part rewrite contract ≤150 words:** Deliverable · Start from · Method · Done when · Not in scope | Bloated prompts; persona lines ("You are a world-class…") |

## Results

Three real projects (one open-source, two private), each run with the skill and as a control (the raw four
questions, same read access). Full tables are in
[`tests/results.md`](tests/results.md).

| | With skill (v2–v3) | Control |
|---|---|---|
| Kept the user's deliverable (or its smallest correct form) | 3/3 | 0/3 |
| Read real raw data and surfaced a decisive, file-verified fact | 3/3 | 3/3 |
| Rewritten prompt length | 119–176 words | ~280–400 words |
| Whole reply | ~500–600 words | ~900–1100 words |
| "Done when" names the failure it catches and a known-bad input | 3/3 | 0/3 |

An example of a decisive fact, from an LLM-council app. In a saved run, all
four judges ranked the same answer first. The chairman model, whose own
answer disagreed, declared "Co-Winners". It was also receiving model names
while the rankings used anonymous labels, with no mapping between them. The
skill's rewrite turned "make the chairman's answer better" into a fix for
that prompt. A test fails on the current commit until the mapping is
passed. The control turned the same request into a 60-question eval
program.

## Install

**As a Claude Code plugin:**

```
/plugin marketplace add arome3/deepen-prompt
/plugin install deepen-prompt@deepen-prompt
```

**As a personal skill (gives you `/deepen-prompt`):**

```bash
git clone https://github.com/arome3/deepen-prompt.git ~/src/deepen-prompt
ln -s ~/src/deepen-prompt/skills/deepen-prompt ~/.claude/skills/deepen-prompt
```

Restart Claude Code, or start a new session, so it picks up the skill.

## Use

- `/deepen-prompt <your task>` deepens that task.
- `/deepen-prompt` on its own deepens your previous request.
- Natural language works too: "make this deeper, not bigger", "what would a
  top pro do here?", or paste the four-question prompt.
- "Deepen it and do it" skips the confirmation and runs the rewritten prompt.

It works best inside the project the task is about, where it reads your
specs, data and test config before answering. Elsewhere it answers from
domain knowledge and marks unseen sources `(verify)`.

## What's in the box

```
skills/deepen-prompt/
  SKILL.md                     the method: scope rule, grounding, four moves,
                               rewrite contract, hand-off format
  references/
    domain-catalog.md          pro moves, raw material, tools and oracles for
                               15 fields (software, debugging, data, ML eval,
                               market/strategy, finance, writing, science,
                               product/UX, legal, security, ops, energy/field,
                               marketing, hiring)
    research.md                origin, the evidence behind each move, and
                               the baseline failures that shaped the rules
tests/
  cases.md                     baseline and real-workspace cases, hand-judged
                               criteria
  check_output.py              mechanical checks on a reply (length, persona,
                               falsifiable Done-when, cited paths exist)
  results.md                   v1 vs v2 vs control
```

## Evidence behind the rules (short version)

- **Practices, not personas.** Expert personas don't improve factual
  accuracy (Zheng et al., EMNLP Findings 2024; Wharton Prompting Science
  Report 4, 2025). The value of question 1 is the concrete practice it
  surfaces.
- **Raw beats digested.** 33–40% of science press releases exaggerate
  (Sumner et al., *BMJ* 2014). LLM summaries had ≈4.85× higher odds of
  overgeneralising than human ones (Peters & Chin-Yee 2025).
- **Outside checks, not self-review.** LLMs don't reliably self-correct
  without external feedback (Huang et al., ICLR 2024; Kamoi et al., *TACL*
  2024), and LLM judges prefer their own outputs (Panickssery et al.,
  NeurIPS 2024).

Full citations are in
[`references/research.md`](skills/deepen-prompt/references/research.md).

## License

MIT
