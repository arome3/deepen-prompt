---
name: deepen-prompt
description: >-
  Use when the user asks for a deeper, more rigorous, or expert-grade version
  of a task or prompt ("deeper, not bigger", "what would a top pro do here",
  "make this more ambitious", "level this up properly"); asks what a
  professional would start from, use, or check for a task; or pastes a prompt
  beginning "I want a deeper version of this task, not a bigger one".
---

# Deepen, don't enlarge

Answers Felix Rieseberg's four questions — what would a top professional do
that I'm not asking for; what is the rawest material; which specific methods
and tools; what, other than you or me, shows it's right — then rewrites the
user's prompt to ask for exactly that. Source and evidence:
`references/research.md`.

You already know what experts do. Tested without this skill, agents
answered all four questions well, then turned "deeper" into "bigger"
(a function → a pipeline; one slide → a GIS project), listed 6–8 unranked
items per question, and wrote 400-word rewrites full of blanks. The job is
**selection, proportion, grounding, and shape**.

**Input:** the task the user gave with the request. No task given → deepen
the user's previous request in this conversation.

## The scope rule

**Enlargement = anything not needed for the result to be correct or for the
outside check.** Extra effort may go only to rawer input, a stronger
method, or an outside check — no new deliverables, phases, or audiences.
Keep the user's deliverable. If correctness *requires* a different form
(a NOT NULL migration on a large table → expand/contract; a TAM from a
report headline → a bottom-up count), rewrite into the **smallest correct
form** and say why in one line. Anything else bigger goes in "Not in scope".

## Process

### 0. Ground — read the raw material itself

If you have tools and the task concerns the current workspace, spend ≈10
read-only calls (not counting this skill's files) on:

1. **The project's own rules and plans** that bear on the task —
   `CLAUDE.md`/`AGENTS.md`, specs, playbooks, decision logs. A conflict
   ("the plan defers this", "the form needs this first") is often the most
   decisive move-1 item.
2. **One actual instance of the rawest material** — a saved run, a data
   row, a log, a trace, a call record — read in full, not just its
   structure. Report one concrete thing it shows (the **Found** line).
3. **The test runner or CI config** — often the oracle's command.

Reading data is the point; limit only what you *copy into the prompt*:
paths (exact, relative to the workspace root), schemas, counts, short
non-sensitive quotes — never PII or secrets
(`.env` values, keys). Never query production. Unrelated or mixed
workspace → skip step 0.

Don't stop to ask questions. Anything only the user can supply becomes a
`[bracket]`; up to 2 questions go after the rewrite.

### 1–4. The four moves — select, rank, don't list

Order each move's items **most decisive first**; the first item alone
should change the result. Each item is one line, ≤25 words; **≤10 items
across all four moves.**

| Move | Selection rule | Keep |
|---|---|---|
| **1. What a top pro would do** | Only items whose absence makes the result *wrong*. Lead with what must be defined or decided first — including whether the project's own plans say to do it now, or this way. If the ask embeds a belief (a cause, a number, "it's X's fault"), one item tries to break it from raw data. | 1–3 |
| **2. Rawest material** | Climb the rawness ladder as far as access allows. Name the *specific* source — path, table, endpoint, dataset, document — with an access tag. | 1–3 |
| **3. Methods & tools** | Real, named (library, command, technique, standard), each serving a move-1 item. Only what the user can run now or with one install. | 2–4 |
| **4. What shows it's right — not you, not me** | Pick by the **named likely failure**: the check that would catch it. Must be fixed before the work starts and shown failing once. | 1–3 |

Before moves 2–4, open the matching section of
`references/domain-catalog.md` (two sections max for cross-domain tasks);
pick from it, don't copy it.

**Specificity test:** every item names something a third party could check
was done — a file, dataset, command, tool, standard, number, or named
person. "Use data-driven insights" or "follow best practices" is
vocabulary, not method.

**Rawness ladder:** the event / measurement / document itself → raw export
or sample → logs, traces, transcripts → dashboard or aggregate → report or
summary → model memory. Tags: `found: <path>` · `you have it` ·
`not accessible → <next rung>` · `doesn't exist → <next rung>; instrumenting
it goes in Not in scope`. Mark a source you haven't seen `(verify)`; never
invent dataset names or figures.

**Oracles** — roughly from hardest to game to easiest; choose by the named
failure, not by rank:
execution or reality (tests, repro stops, meter reading, money received) ·
prediction written before running, scored after · independent system of
record (filing, registry, ledger, regulator record) · invariant (totals
that must not move, reconciliation, round-trip) · formal checker (types,
schema, compiler, axe) · pre-registered metric vs control (A/B, holdout) ·
a named human, blind, applying a rubric they didn't write · an adversary or
market (pentest, paying customer).

The executor can't be its own oracle: self-review, "I double-checked", and
the user's approval don't count. Another model with a fixed rubric counts
only alongside one of the above. Skip generic "verify your work" lines.

**Proportion:** the check is the cheapest one that catches the named
failure, with at least one runnable today. When the deliverable *is* a
check (a test, audit, review, eval) or the failure is intermittent, the
check is the task — size it to the failure rate.

### 5. Rewrite — the contract

Five parts, in order, **≤150 words** total:

1. **Deliverable** — the user's deliverable (or its smallest correct form),
   with any target set at the top-professional bar, stated as reachable.
2. **Start from** — the raw material, with paths/sources you found.
3. **Method** — the named methods/tools.
4. **Done when** — `<check>`, which fails if `<named failure>` (keep the
   words "fails if"); seen failing on `<parent commit / planted error /
   known-bad input>` — an input the work could wrongly pass, not just "the
   work isn't done yet"; unchanged after the work starts.
5. **Not in scope** — one line naming the bigger version you left out.

Write what the professional *does*; no persona line ("You are a world-class
X") — personas change vocabulary, not accuracy. Found facts go in as facts;
a `[bracket]` survives only for what the user alone can supply. The rewrite
doesn't re-explain the moves above it.

### 6. Hand off — whole reply ≤500 words

```
**Deeper, not bigger:** <one sentence — what this task really is>
**Found:** <≤2 sentences: one concrete fact from the raw material or project rules, with path>
           (omit only when step 0 was skipped)

1. **What a top pro would do** — …
2. **Rawest material** — … (found: path · you have it · next rung)
3. **Methods & tools** — …
4. **What shows it's right (not you, not me)** — …

**Rewritten prompt:**
> …

<one line of assumptions, or ≤2 questions>
Run it now?
```

**Before sending, measure — don't estimate:** run `wc -w` on the rewrite and
the whole reply (draft them to a scratch/temp file outside the project), or
count by hand. Over 150 / 500 → cut the least decisive
items from moves 2–3 first, then tighten wording. Agents in testing
overran both limits whenever they estimated.

If the user already asked you to execute ("deepen and do it"), skip the
question and run the rewritten prompt.
