# qa-orchestrator

A Claude Code multi-agent QA system. Point it at an application's source code you own, and it runs a full quality assessment — functional, non-functional, API, GDPR/compliance, and offensive + defensive security review — then produces a single prioritised HTML report.

This is primarily **static, read-only analysis** — most agents work purely by reading source code, and nothing is run, built, deployed, or sent live traffic. The one exception is the `Database Testing Agent`, which, where Docker is available, spins up the application's database in an isolated container to verify migrations, seed data, and query correctness.

## How it works

**`QA Test Lead`** (Opus, medium reasoning) is the orchestrator. It dispatches six specialist subagents, merges and deduplicates their findings, and writes the final report.

| Specialist | Focus | Model | Reasoning |
|---|---|---|---|
| `Functional Testing Agent` | User journeys, acceptance criteria, regression risk, edge cases | Sonnet | High |
| `Non Functional Testing Agent` | Performance, accessibility, usability, reliability, scalability, compatibility, maintainability | Sonnet | Low |
| `API Testing Agent` | Contracts, request/response validation, status codes, error handling, auth, data validation, integration risk | Sonnet | Medium |
| `GDPR and Compliance Agent` | Personal data handling, consent, retention, minimisation, compliance gaps | Sonnet | Medium |
| `Database Testing Agent` | Data integrity, relationships, constraints, migrations, seed data, transactions, database-driven business rules — runs live against an isolated Docker container where available | Sonnet | Medium |
| `Security Attack Agent` | Vulnerabilities, abuse cases, injection, auth/authorization weaknesses, exposed data (red team) | Sonnet | High |
| `Security Defence Agent` | Mitigations and preventative controls, reviewing the Attack Agent's findings (blue team) | Sonnet | High |

Orchestration order: `Functional`, `Non Functional`, `API`, `GDPR`, and `Database` run in parallel (they're independent). `Security Attack` then runs, and its findings are fed into `Security Defence`, which must run after it.

## Usage

Open Claude Code in this directory and ask it directly to run a QA assessment against a target app, for example:

> Use the QA Test Lead agent to run a full QA assessment on `/home/jason/code/some-other-app`

The QA Test Lead will dispatch every specialist, merge their findings, and write a report to `reports/`.

## Output

Each run produces `reports/<date>_<app-name>.html` — a self-contained HTML file you can open directly in a browser. It includes:

- A summary section (finding counts by severity, exec summary, which agents ran)
- A single findings table, sorted highest severity to lowest, with columns: **Severity, Agent, Issue, Impact, How to Replicate, Recommendation**

`reports/` is gitignored — findings are often sensitive (real vulnerabilities, compliance gaps) about whatever app you point this at, so they stay local and are never committed.

## Project structure

```
qa-orchestrator/
├── .claude/agents/           # Subagent definitions (the QA Test Lead + 6 specialists)
├── templates/
│   └── report-template.html  # The HTML shell the QA Test Lead fills in per run
├── reports/                  # Generated reports (gitignored)
└── docs/
    └── adding-a-new-agent.md # How to add another specialist QA agent
```

## Extending it

See [`docs/adding-a-new-agent.md`](docs/adding-a-new-agent.md) — adding a new specialist is one new agent file plus wiring it into the QA Test Lead's dispatch list.

## Notes

- Only point this at code you own or are authorised to review — the Security Attack Agent reasons about real exploit paths, which is only appropriate for authorised review of your own application.
- Not legal advice: the GDPR and Compliance Agent flags code-level risk signals for a human/legal review, not a definitive compliance judgment.
