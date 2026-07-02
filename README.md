# agentic-qa-orchestrator

A Claude Code multi-agent QA system. Point it at an application's source code you own, and it runs a full quality assessment — functional, non-functional, API, GDPR/compliance, database, and offensive + defensive security review — then produces prioritised HTML and JSON reports.

By default this is **static, read-only analysis**. If you explicitly authorize dynamic testing, specialists may run the app and supporting services locally, preferably in isolated Docker containers, and send traffic only to localhost/loopback targets. They must never modify the target app or send traffic to non-localhost systems.

## How it works

**`QA Test Lead`** (Opus, medium reasoning) is the orchestrator. It builds a shared Discovery Packet, conditionally dispatches seven specialist subagents, merges and deduplicates their findings, and writes the final reports.

| Specialist | Focus | Model | Reasoning |
|---|---|---|---|
| `Functional Testing Agent` | User journeys, acceptance criteria, regression risk, edge cases | Sonnet | High |
| `Non Functional Testing Agent` | Performance, accessibility, usability, reliability, scalability, compatibility, maintainability | Sonnet | Medium |
| `API Testing Agent` | Contracts, request/response validation, status codes, error handling, auth, data validation, integration risk | Sonnet | Medium |
| `GDPR and Compliance Agent` | Personal data handling, consent, retention, minimisation, compliance gaps | Sonnet | Medium |
| `Database Testing Agent` | Data integrity, relationships, constraints, migrations, seed data, transactions, database-driven business rules — can run live against an isolated local database when dynamic testing is authorized | Sonnet | Medium |
| `Security Attack Agent` | Vulnerabilities, abuse cases, injection, auth/authorization weaknesses, exposed data (red team) | Sonnet | High |
| `Security Defence Agent` | Mitigations and preventative controls, reviewing the Attack Agent's findings (blue team) | Sonnet | High |

Orchestration order: the QA Test Lead first builds a shared Discovery Packet, then conditionally runs relevant independent specialists in parallel. `Security Attack` then runs when there is an attack surface, and its findings are fed into `Security Defence`, which must run after it.

## Usage

Open Claude Code in this directory and ask it directly to run a QA assessment against a target app, for example:

> Use the QA Test Lead agent to run a full QA assessment on `/home/jason/code/some-other-app`

To allow local dynamic verification:

> Use the QA Test Lead agent to run a full QA assessment on `/home/jason/code/some-other-app`. Dynamic testing is authorized on localhost only.

The QA Test Lead will build a shared Discovery Packet, dispatch the relevant specialists, merge their findings, and write reports to `reports/`.

## Output

Each run produces:

- `reports/<date>_<app-name>.html` — a self-contained HTML file you can open directly in a browser.
- `reports/<date>_<app-name>.json` — the same normalized report data for diffing, ticket creation, or automation.

The HTML report includes:

- A summary section (finding counts by severity, exec summary, which agents ran)
- A single findings table, sorted highest severity to lowest, with columns: **Severity, Confidence, ID, Agent, Issue, Impact, Evidence, How to Replicate, Recommendation**

`reports/` is gitignored — findings are often sensitive (real vulnerabilities, compliance gaps) about whatever app you point this at, so they stay local and are never committed.

## Project structure

```
agentic-qa-orchestrator/
├── .claude/agents/           # Subagent definitions (the QA Test Lead + 7 specialists)
├── templates/
│   └── report-template.html  # The HTML shell the QA Test Lead fills in per run
├── reports/                  # Generated reports (gitignored)
└── docs/
    └── adding-a-new-agent.md # How to add another specialist QA agent
```

## Extending it

See [`docs/adding-a-new-agent.md`](docs/adding-a-new-agent.md) — adding a new specialist is one new agent file plus wiring it into the QA Test Lead's dispatch list.

For the machine-readable output shape, see [`docs/report-schema.md`](docs/report-schema.md).

## Notes

- Only point this at code you own or are authorised to review — the Security Attack Agent reasons about real exploit paths, which is only appropriate for authorised review of your own application.
- Not legal advice: the GDPR and Compliance Agent flags code-level risk signals for a human/legal review, not a definitive compliance judgment.
