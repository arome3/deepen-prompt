# Results

Three real projects (see `cases.md`; two are private and are described, not named), run on 14 Oct 2026 with Claude Opus 5.5
subagents. Each skill run read the project with read-only access. Each control
got the original four-question prompt with the same access and was told not
to read this repo. Mechanical scores come from `skills/deepen-prompt/scripts/check_reply.py` (named `tests/check_output.py` before v5). "Found"
facts were spot-checked against the files by the orchestrating session.

## Mechanical checks

| Run | Reply words | Rewrite words | Done-when names failure + known-bad input | Cited paths exist |
|---|---|---|---|---|
| Control T1 llm-council | ~1100 | ~400 | no | yes |
| Control T2 AI-receptionist pricing | ~1100 | ~300 | no | yes |
| Control T3 B2B launch post | ~900 | ~280 | no | yes |
| v1 T1 / T2 / T3 | 450 / 461 / 452 | 147 / 158 / 149 | 3/3 | 3/3 |
| v2 T1 / T2 / T3 | 504 / 511 / 501 | 143 / 119 / ~150 | 2/3 | 2/3 (one path missing its folder) |
| v3 T1 / T2 / T3 | 595 / 607 / 619 | 176 / 154 / 146 | 3/3 | 3/3 |
| v4 T1 / T3 | 464 / 438 | 147 / 148 | 2/2 | 2/2 (one flag was a true finding: a file the project's docs mention that doesn't exist) |
| v4 user run, private energy-platform repo (first held-out case) | n/a (rewrite only) | 161 | named failure yes; seen failing only on "the current version scored against itself" | 2 wrong: a script path missing its top folder, an ambiguous `metrics.py` (4 in repo) |
| v5 solar #1 / #2 (same task, re-run) | 405 / 422 | 121 / 132 | 2/2 | 2/2 |
| v5 T1 regression | 462 | 150 (177 on first draft; checker caught it) | 1/1 | 1/1 |
| v5 held-out: "write the pitch for our next pilot operator" | 440 | 130 | 1/1 (grep for stale offer terms, run on the old playbook first and seen matching) | 1/1 (6 cited) |

## Judged by hand

| | Controls | v1 | v2 / v3 |
|---|---|---|---|
| Kept the user's deliverable (or its smallest correct form) | 0/3. Grew into a 60-question eval program, a 5-output pricing study, and a readiness-gated campaign | 3/3 | 3/3 |
| Read an actual raw instance and surfaced a decisive fact | 3/3 | 0/3 (stayed at doc/structure level) | 3/3 |
| Checked the project's own plans/rules against the task | 2/3 | 1/3 | 3/3 |

Decisive facts the v2/v3 skill runs surfaced, all verified in the files:

- **llm-council:** in saved run `c63147d6`, all four judges ranked
  Response A (gpt-5.1 → Perplexity) first, and the chairman (Gemini,
  whose own answer picked Neuralink) declared "Co-Winners". Stage 1 reaches
  the chairman under model names while rankings use "Response A–D", and no
  mapping is passed (`backend/council.py:133-141`).
- **AI-receptionist pricing (private project):** the validation tracker
  held only example rows, and the lab call reports had durations but no
  cost fields. The spec said per-minute costs were "not sourced yet", while
  the pilot offer locked a founding price for 12 months.
- **Pre-launch B2B company (private project):** the site's call-to-action
  destination was `null`. The company's own growth playbook said the
  current stage is founder outbound, "not … LinkedIn volume". The only
  evidence sample was marked not sendable.

## What changed between versions, and why

| Version | Change | Evidence that drove it |
|---|---|---|
| v1 | Scope rule, ranked moves, rawness ladder, oracle ladder, five-part contract | 4 baseline runs (see `cases.md`) |
| v1.1 | "Smallest correct form" scope rule; oracle picked by named failure and shown failing; no persona; privacy limits | 2 independent reviews |
| v2 | Step 0 reads one **actual instance** of raw data and the project's own plans; **Found** line | v1 lost to controls on digging: "never paste record contents" was read as "don't read records" |
| v3 | ≤10 items total; Found ≤2 sentences; the literal words "fails if"; paths relative to root | v2 overran the 400-word cap 3/3; one wrong path; one Done-when without a named failure |
| v5 | The skill runs `scripts/check_reply.py` on its draft before sending: word limits, five labels, Done-when, paths relative to root (prints the right path). "Seen failing on" must be an input that commits the named failure; the unchanged work scored against itself is ruled out | The user's first held-out run still overran 150 words, had a path missing its folder (as in v2) and an ambiguous path, and a check seen failing only against itself. Prose rules had already failed to fix these, so a script now enforces the mechanical ones |
| v4 | Measure with `wc -w` before sending; known-bad input must be one the work could wrongly pass | v3 overran 500 words 3/3 and 150 words once. Estimated limits kept drifting upward as caps were raised. One "seen failing" was trivially true ("0 of 5 signed today") |

## v5 runs, judged by hand

All Found facts were checked against the files by the orchestrating session.

- **Solar forecast (both runs):** found that a weather-physics forecast already
  exists but is switched off, because its only evidence (+34 % / +51 % CRPS
  skill on two US sites) used short-lead weather, while the day-ahead floor
  was 0 % / +20 %. Both kept the day-ahead question; run 1 reframed the
  deliverable as a go/no-go on the switch, run 2 kept "a change that lowers
  CRPS". Both chose a no-skill baseline (`weather_persistence`) as the
  seen-failing input: better than "against itself", but not one of the named
  failures (short-lead weather, tuning on the test period). The checker can't
  judge that match.
- **Held-out pitch:** found that the next operator call was booked for the
  next day, that the operator is "paid only" under the current offer kit
  while an older playbook still offered it a free pilot at $100/site/month,
  and wrote a grep oracle that matched the stale playbook. Miss: the
  operator had asked "show us a site record" and was promised that walk-
  through; the talk track leads with qualifying questions and makes the data
  view conditional. Scope held (one talk track; deck, ROI model and other
  operators out).

## Honest limits

- n = 1 run per cell; the variance between runs is visible in the table.
- Reply length was the hardest contract term to hold. Depth (the Found
  line, project-rule checks) costs words, and the skill's replies run
  about half the controls' length, not a fixed size.
- The hand judgements were made by the same session that wrote the
  skill. The mechanical checks and the file-verified facts are the parts
  that don't depend on that judgement.

- Grounding used 7–16 tool calls (budget ≈10). The extra calls went to
  reading project plans, which is where the decisive facts were.
