# Why this works — evidence base

Not needed to run the skill. Read when the user asks *why*, or when you need
to justify a move (e.g. refusing a persona line, refusing "have another AI
check it").

## Origin

Felix Rieseberg (engineering manager at Anthropic: Claude.ai, Cowork,
Claude Code Desktop; Electron co-maintainer), **"How to be more ambitious: A tutorial
for humans with models"**, 13 Oct 2026 —
https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/

The prompt, verbatim (introduced as "A simple prompt that often helps me"):

> I want a deeper version of this task, not a bigger one. Before rewriting it:
> (1) say what a top professional in this field would do here that I'm not
> asking for; (2) name the rawest material they would start from instead of
> what has already been digested for me; (3) name the specific methods and
> tools they would use; (4) say what, other than you or me, would show the
> result is right. Then rewrite my prompt to ask for exactly that.

The prompt sits under **Depth** — one of four kinds of ambition (Speed,
Altitude = outcome not task, Depth, Range = cross-field). Depth: "considering
a task the way a field-leading expert would … go one level deeper and touch
the underlying data, tools, and problems."

Caveats from the post that shape this skill:
- "Models often switch vocabulary without actually switching methods" →
  every item must name a checkable artefact, not expert-sounding words.
- (From the post's Range section) role play "will make your transcript weirder without improving the actual
  outcome … Don't ask the model to write a short seller, ask it to do what a
  short seller does" → no persona lines in the rewrite.
- "Do not ask the model to judge itself … insist on outside validation.
  Ideally that's a tool the model can run to get feedback immediately." →
  move 4, oracle ladder, prefer runnable checks.
- Depth assumes the model has a computer and access to the data → step 0
  (ground in the environment) and access tags on raw material.

## Move 1 — expert practice, not expert persona

- Experts represent problems by deep principle, novices by surface features
  (Chi, Feltovich & Glaser 1981, *Cognitive Science* 5:121–152).
- Experts hold tacit knowledge they don't volunteer; cognitive task analysis
  exists to elicit it (Crandall, Klein & Hoffman, *Working Minds*, 2006).
  Expert blind spot: experts skip steps novices need (Nathan & Petrosino
  2003, *AERJ* 40:905) → the "can the user actually run this?" check.
- Personas don't improve accuracy: Zheng et al., Findings of EMNLP 2024
  (162 roles; arXiv 2311.10054); Wharton Prompting Science Report 4, Dec
  2025 ("Playing Pretend: Expert Personas Don't Improve Factual Accuracy",
  arXiv 2512.05858) — recommends task-specific instructions instead.
- Step-back prompting (abstract to principles first) helps reasoning
  (Zheng et al., ICLR 2024, arXiv 2310.06117) — the "reframe" line.

## Move 2 — raw beats digested

- 33–40% of university press releases contained exaggeration (advice 40%,
  causal claims 33%, animal-to-human 36%); news exaggeration
  tracks it (Sumner et al., *BMJ* 2014, g7015).
- LLM summaries of science had ≈4.85× higher odds of overgeneralising than
  human-written ones (OR 4.85, 95% CI 3.06–7.70), and
  "be accurate" prompts made it worse (Peters & Chin-Yee, *R. Soc. Open
  Sci.* 2025, doi 10.1098/rsos.241776).
- Citation quotation errors ≈ 25% (11.9% major) in medicine (Jergas &
  Baethge 2015, PMC4627914).
- Aggregation hides structure: Simpson's paradox, Anscombe's quartet.
- Practitioner norms: Karpathy "become one with the data" (2019); Husain &
  Shankar error analysis — read the traces before choosing metrics.

## Move 3 — named methods change the procedure

- Running a tool beats imitating it: PAL (Gao et al., ICML 2023) — code
  executed by an interpreter beats chain-of-thought by ~15 pts on GSM8K;
  letting the model "execute" its own code collapses accuracy.
- Named methods carry known failure modes and validation literature, and
  make output auditable.

## Move 4 — outside verification

- Intrinsic self-correction fails without external feedback (Huang et al.,
  ICLR 2024, arXiv 2310.01798; Kamoi et al., *TACL* 2024; Stechly et al.
  2023/2024). Sound external verifiers work (Kambhampati et al. LLM-Modulo,
  ICML 2024; CRITIC, ICLR 2024).
- LLM judges prefer their own outputs (Panickssery, Bowman & Feng, NeurIPS
  2024) and show position/verbosity bias (Zheng et al. 2023, MT-Bench).
- The user is a compromised oracle too: sycophancy (Sharma et al., ICLR
  2024).
- Test-oracle problem: oracles come from specs, models, contracts,
  metamorphic relations (Barr et al., *IEEE TSE* 2015).
- Over-verification: Anthropic's Opus 5 prompting guide notes generic
  "verify your work" instructions cause over-verification without quality
  gain, and that the model "can also expand the scope of a task, adding
  steps that weren't requested" —
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Padded inputs degrade reasoning well below context limits (Levy, Jacoby &
  Goldberg, ACL 2024, arXiv 2402.14848). That study used much longer
  inputs than a prompt rewrite, so the 150-word contract rests mainly on the
  baseline tests below, not on it. Anthropic's Opus 5 guide also says the
  model does best with the complete task specification up front — hence
  the contract keeps every *decision-relevant* fact and cuts only padding.

## Reviews that shaped v1

Two independent reviews (authoring quality; adversarial method fidelity)
led to: the scope rule ("enlargement = anything not needed for correctness
or the outside check") replacing a blunter "same deliverable noun" rule that
would have blocked necessary reshaping (e.g. expand/contract migrations);
choosing oracles by a *named likely failure* and showing them fail once;
adding "challenge what you know" and top-pro-bar targets from the post;
and privacy limits on workspace grounding.

## Tests that shaped v2–v4

Head-to-head runs on three real projects (an open-source LLM-council app; two
private projects: an AI receptionist's pilot pricing and a pre-launch B2B
company's LinkedIn post): v1 kept
the deliverable but lost to controls on *digging*, because "never paste
record contents" was read as "don't read records". v2 added "read one
actual instance of raw data + the project's own plans" and the Found line,
which closed the gap. Length caps were overrun whenever agents estimated
instead of measuring, hence the `wc -w` step. Details: `tests/results.md`
in the repo.

## Baseline tests that shaped the skill

Four agents answered the original prompt without this skill (dedup
function, mini-grid market slide, slow React app, fasting newsletter).
All showed strong domain knowledge. Three of four turned "deeper" into
"bigger" (function → entity-resolution pipeline; slide → GIS modelling
project; diagnosis → 7-step program with 5 attachments). All produced
unranked lists of 6–8 items per move, rewrites of 300–450 words for
10–15-word asks, `[fill in]` brackets for facts an agent could look up, and
verification sized out of proportion to the task. The one agent given only
"make it deeper, not bigger" stayed small but stayed shallow — it still
asked the model to summarise from memory, with no raw source or outside
check.
