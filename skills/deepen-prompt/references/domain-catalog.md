# Domain catalog

Starting points for the four moves in 15 fields. **Select from these, don't
copy them** — pick the 1–3 per move that would change *this* task's result,
and prefer what you can verify exists in the user's environment. Tool names
are canonical but were not individually re-checked; mark anything you cite
to the user `(verify)` if you have not seen it work.

Key: **Pro** = what a top professional does that amateurs don't ask for ·
**Raw** = rawest material · **Tools** = named methods/tools · **Oracle** =
what, other than the author or the AI, shows it's right.

Contents: [Software](#software-engineering-feature-work) ·
[Debugging/perf](#debugging--performance) · [Data](#data-analysis--analytics) ·
[ML/AI eval](#ml--ai-evaluation) · [Market/strategy](#market-research--strategy) ·
[Finance](#finance--fundraising) · [Writing](#writing--journalism--content) ·
[Science](#academic--scientific-research) · [Product/UX](#product--ux) ·
[Legal](#legal--compliance--policy) · [Security](#security) ·
[Ops/infra](#ops--infra--devops) · [Energy/field](#energy--hardware--field-ops) ·
[Marketing](#marketing--growth) · [Hiring](#hiring--people)

## Software engineering (feature work)
- **Pro:** read call paths and history before designing; failing acceptance test first; flag + rollback plan; migration/backfill and backward compatibility; threat-model new inputs; record rejected alternatives.
- **Raw:** call sites (`rg`, LSP references); `git log -S'<sym>'`, `git log -L`, `git blame` + linked PRs/issues; real DB schema (`\d+` in psql), not the ORM model; prod logs/traces for the endpoint; the originating ticket.
- **Tools:** TDD; property-based tests (Hypothesis, fast-check); contract tests (Pact); `tsc --strict`/mypy/pyright; feature flags (OpenFeature); expand/contract migrations; mutation testing (Stryker, mutmut).
- **Oracle:** test written first and *seen failing*; type/lint exit codes; canary error rate vs SLO; mutation score; a real user completing the task.

## Debugging / performance
- **Pro:** minimal repro first; bisect before theorising; measure before optimising, with a falsifiable hypothesis; check recent deploys/config; separate p50 from p99 and lab from field; find the *first* error, not the loudest; leave a regression test.
- **Raw:** full stack traces / core dumps; raw logs with trace IDs; `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`; strace/dtrace; packet captures; field RUM (web-vitals attribution, CrUX, Long Animation Frames) — not one Lighthouse score; the exact failing input.
- **Tools:** `git bisect run`; rr; perf + FlameGraph, pprof, py-spy, Scalene, clinic.js, Instruments; bpftrace; USE/RED methods; Chrome Performance panel (INP breakdown); React Profiler; WebPageTest; sanitizers (ASan/TSan/UBSan); delta debugging.
- **Oracle:** repro script fails on parent commit, passes on fix; benchmark with confidence intervals (hyperfine, benchstat); field p75 after deploy; error fingerprint stays resolved.

## Data analysis / analytics
- **Pro:** ask what decision this serves; provenance and instrumentation-change history; define metrics before looking; check sample-ratio mismatch, survivorship, Simpson's paradox by segment; report uncertainty; Twyman's law ("surprising = probably wrong").
- **Raw:** event-level tables (GA4 BigQuery `events_*`, Segment/Snowplow raw); app DB snapshot; payment ledger (e.g. Stripe `balance_transactions`); tracking plan + changelog; raw survey text.
- **Tools:** SQL in DuckDB/BigQuery; dbt tests, Great Expectations; cohort/retention curves; Kaplan–Meier (lifelines); diff-in-diff, synthetic control; CUPED; bootstrap CIs.
- **Oracle:** reconcile to an independent ledger (warehouse ↔ payments ↔ bank); A/A test; SRM chi-square; held-out-period backtest; pre-registered decision rule; second analyst reproduces from raw.

## ML / AI evaluation
- **Pro:** error analysis *before* picking metrics; production-representative held-out set; contamination check; judge calibrated against humans; confidence intervals; slice analysis; tie metric to the user outcome.
- **Raw:** production traces (inputs, tool calls, outputs); user edits/regenerations/thumbs; raw annotations with annotator IDs; failures from support tickets.
- **Tools:** read 50–100 traces and open/axial-code failures (Husain & Shankar); Inspect, promptfoo, lm-eval-harness; Cohen's κ / Krippendorff's α; paired bootstrap / clustered SEs; judge TPR/TNR vs human labels; ablations.
- **Oracle:** blind human labels on a held-out set; execution checks (unit tests, exact match); judge–human agreement above a pre-set bar; online A/B on a user outcome. *Not* the same model grading itself (self-preference bias).

## Market research / strategy
- **Pro:** bottom-up sizing (units × price × reachable), not "1% of $XB"; find the binding constraint; the assumption that kills the thesis; competitor unit economics from filings; willingness-to-pay evidence; write the bear case.
- **Raw:** filings (SEC EDGAR 10-K/S-1, XBRL facts; national registries); earnings-call transcripts; national statistics / World Bank WDI; tender and procurement records; pricing pages via Wayback; job postings; review text; interview recordings.
- **Tools:** JTBD/switch interviews, The Mom Test; Van Westendorp / Gabor–Granger; conjoint/MaxDiff; reference-class adoption curves; fake-door tests.
- **Oracle:** 2–3 independent sizing methods that converge; reconcile with a public competitor's revenue or a regulator's registered count; LOIs, pre-orders, paid pilots; fake-door conversion vs a pre-set threshold.

## Finance / fundraising
- **Pro:** model ties out on cash; sensitivity on the 2–3 drivers that matter; cohort unit economics (CAC payback, gross-margin LTV); dilution through future rounds + option pool; non-price terms (liquidation preference, pro-rata, board, protective provisions).
- **Raw:** general ledger and bank statements; payment-processor payouts; cap-table ledger; executed SAFEs/notes; contracts and invoices.
- **Tools:** three-statement model; DCF/comps; net-revenue-retention cohort waterfalls; Monte Carlo on drivers; post-money SAFE math; blended / results-based finance structures (energy access).
- **Oracle:** balance sheet balances and cash ties to bank; CPA review/audit or QoE; investor counsel's redline; market benchmarks (Carta, Cooley reports); wired funds.

## Writing / journalism / content
- **Pro:** report before writing; know the one sentence the piece exists to say; find the counter-source; right of reply; line-by-line fact-check; lead with the news; cut 30%.
- **Raw:** the original study/dataset, not the press release; court records (CourtListener); company registries (OpenCorporates, Companies House, Nigeria CAC); FOIA responses; interview audio; Wayback snapshots; the user's own product docs/specs.
- **Tools:** discipline of verification; SIFT / lateral reading; reverse image search; DocumentCloud, Datasette, OpenRefine; inverted pyramid / nut graf.
- **Oracle:** every claim links to a primary document a reader can open; two independent sources for key facts; the subject's reply; 5 target readers restate the main point unaided; downstream reply/click rate vs a baseline post.

## Academic / scientific research
- **Pro:** systematic search; read methods and supplements, not abstracts; check replication and retraction status; strongest rival explanation; effect sizes with CIs; power analysis; pre-register.
- **Raw:** full text + supplements; trial registries (ClinicalTrials.gov, WHO ICTRP) results tabs; shared data/code (OSF, Zenodo, Dryad); instrument output files; published peer-review files.
- **Tools:** PRISMA 2020; Cochrane RoB 2; GRADE; metafor; G*Power; statcheck/GRIM; Retraction Watch via Crossref; OpenAlex / Semantic Scholar APIs.
- **Oracle:** computational reproduction from shared data; independent replication; pre-registered prediction confirmed; statcheck/GRIM consistency; triangulation across methods.

## Product / UX
- **Pro:** the job/problem before screens; observe users in context; design empty, error, edge, and accessibility states; prototype the riskiest assumption first; success metric + guardrails; reuse the design system; copy is design.
- **Raw:** session recordings; support tickets and sales-call transcripts; raw usability video; site-search logs; user-level funnel events; rage/dead clicks.
- **Tools:** contextual inquiry; think-aloud usability tests; Nielsen heuristics; tree testing / card sorting; opportunity solution tree; WCAG 2.2 AA via axe-core + manual screen reader.
- **Oracle:** task success / time-on-task with 5–8 target users not involved in the design; SUS/SEQ vs benchmark; zero axe violations + screen-reader pass; A/B on a pre-registered metric; fewer tickets for that flow.

## Legal / compliance / policy
- **Pro:** pin jurisdiction and exact instrument version; read the text itself; study actual enforcement; confirm still good law; map obligation → control → evidence; take the regulator's strongest reading.
- **Raw:** consolidated legislation (eCFR, EUR-Lex, legislation.gov.uk, national gazettes, regulator sites); dockets and comments; case law; enforcement decisions; the actual contract + amendments; real data flows.
- **Tools:** IRAC; citators (Shepard's, KeyCite); control mapping (ISO 27001, SOC 2, NIST CSF); DPIA; clause playbooks; compliance matrix with evidence links.
- **Oracle:** licensed counsel's opinion in the jurisdiction; regulator permit/approval; independent audit; every authority verified in a citator (fabricated AI citations are a known failure).

## Security
- **Pro:** threat-model first (assets, actors, trust boundaries); prioritise by exploitability, not CVSS alone; test authZ/IDOR; supply chain; assume breach and test detection; rotate secrets.
- **Raw:** source + IaC; cloud audit logs (CloudTrail etc.); identity-provider logs; flow logs; SBOM of what is actually deployed; full git history for secrets; raw HTTP via proxy.
- **Tools:** STRIDE / attack trees; MITRE ATT&CK; OWASP ASVS / Top 10 / LLM Top 10; Semgrep, CodeQL; Burp, ZAP, nuclei; osv-scanner, Trivy, Syft; gitleaks, trufflehog; CISA KEV + EPSS; fuzzers (AFL++, libFuzzer).
- **Oracle:** PoC exploit works before, fails after the fix; independent pentest; bug bounty; detection fires in a purple-team test of a named technique.

## Ops / infra / DevOps
- **Pro:** SLOs + error budgets from user journeys; limit blast radius; progressive, reversible delivery; *restore-test* backups; capacity from load tests; runbooks; blameless postmortems; drift detection.
- **Raw:** full-resolution metrics; OpenTelemetry traces; structured logs; cloud audit logs; `terraform plan` vs cloud API; k8s events / `kubectl describe`; pager history; billing exports.
- **Tools:** multi-window burn-rate alerts; USE/RED; chaos experiments / game days; k6, Locust; OPA/Conftest, Checkov; Argo CD / Flux; DORA metrics.
- **Oracle:** restore drill meets RPO/RTO; load test holds target RPS at p99; `terraform plan` shows no drift; chaos hypothesis holds; SLO burn within budget.

## Energy / hardware / field ops
(solar mini-grids, C&I solar, IoT fleets)
- **Pro:** size from *measured* load profiles, not appliance surveys; long-term irradiance; battery degradation and replacement capex; O&M access and spares logistics; tariff / ARPU / collection reality; grid-arrival and regulatory risk; remote monitoring from day one; commission against a protocol; log outage causes.
- **Raw:** per-customer smart-meter interval data; inverter/MPPT/BMS logs (cell voltages, SoC/SoH, temperature); SCADA historian; mobile-money payment logs; genset fuel logs; technician tickets + photos; irradiance (NASA POWER, PVGIS, Global Solar Atlas, NSRDB); settlement/building layers (GRID3, Google Open Buildings).
- **Tools:** HOMER Pro (LCOE/NPC); PVsyst, NREL SAM / PVWatts; load-profile generators (RAMP) calibrated to metered comparables (AMDA benchmarks); IEC 62446-1 commissioning (I-V curves, insulation, IR thermography); IEC TS 62257; Modbus/SunSpec, MQTT; anomaly detection on telemetry; 5 Whys / fishbone.
- **Oracle:** metered kWh and uptime % from meters/inverters (not the design model); performance ratio vs modelled yield; collection rate; capacity-test SoH; independent verification agent (results-based-financing programmes); AMDA "Benchmarking Africa's Minigrids" 2024 (pub. 2025) for capex/opex/ARPU sanity checks; NERC (Nigeria) Mini-Grid Regulations 2023 (issued 29 Dec 2023) for permit facts.
- **Telemetry software side:** Raw = meter/inverter frames *before* resampling (gaps, clock drift, counter rollover, kW vs kWh unit mix are the usual traps); Tools = TimescaleDB/InfluxDB continuous aggregates, gap-fill with explicit flags; Oracle = kWh total reconciles between raw frames and the dashboard aggregate, and against a billing/collection ledger.

## Marketing / growth
- **Pro:** incrementality, not attribution; cohort payback by channel; ICP from best customers; message–market fit before spend; separate brand from performance; lifecycle holdouts.
- **Raw:** ad- and day-level platform exports; server-side UTM events; CRM stage history; customer-level revenue; Search Console queries; "how did you hear about us" free text; competitor ads (Meta Ad Library); sales calls.
- **Tools:** geo-lift / CausalImpact; MMM (Meridian, Robyn, PyMC-Marketing) calibrated to lift tests; holdouts; message testing (Wynter); positioning (Dunford).
- **Oracle:** randomised holdout or geo lift with CIs; revenue reconciled to billing — not the ad platform's self-attribution (as circular as a model grading itself); retention of acquired cohorts.

## Hiring / people
- **Pro:** job analysis (outcomes in first 6–12 months); structured interviews with anchored scales; work samples; independent scoring before debrief; specific reference questions; adverse-impact check; onboarding plan.
- **Raw:** artefacts from top performers in the role; the candidate's real work; scorecards written before debrief; pipeline data by stage/source; exit interviews; raw comp data.
- **Tools:** structured interviews (top predictor in Sackett et al. 2022, *J. Appl. Psych.* — re-ranking contested); work-sample tests; scorecards (Smart & Street "Who"); anchored rubrics; blind résumé review; four-fifths rule.
- **Oracle:** interview scores vs 6–12-month performance; inter-rater reliability; work sample graded blind by a non-interviewer; 90-day retention.
