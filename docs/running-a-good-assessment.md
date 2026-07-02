# Running a good assessment

## Before you run

- Confirm the target path points to code you own or are authorized to review.
- Close or remove production secrets from local `.env` files before dynamic testing.
- Prefer a target app checkout with README, sample env files, tests, migrations, and local run instructions present.
- Decide whether dynamic testing is authorized. If yes, say so explicitly and limit it to localhost.

## Recommended prompts

Static review:

```text
Use the QA Test Lead agent to run a full QA assessment on `/path/to/app`.
Do not run the app or send requests.
```

Local dynamic verification:

```text
Use the QA Test Lead agent to run a full QA assessment on `/path/to/app`.
Dynamic testing is authorized on localhost only.
Prefer isolated Docker containers and do not modify the target app.
```

## Good target context

- `README.md` or product notes describing intended behavior.
- `.env.example` or safe local test configuration.
- Package manifests and lockfiles.
- Route/schema/API docs, if available.
- Database migrations, seed scripts, and test fixtures.
- Existing unit, integration, or end-to-end tests.

## After the run

- Open the HTML report and filter by `Critical`/`High` first.
- Check the assumptions and skipped-checks section before treating the report as complete.
- Use the JSON report for diffing, ticket creation, or follow-up automation.
- Treat GDPR/compliance findings as code-level signals for human/legal review, not legal advice.
- Treat security findings as authorized-review hypotheses until verified and fixed.
