# Adding a new specialist QA agent

The system is designed so a new specialist is just one new file plus one line of orchestration wiring.

## 1. Create the agent file

Add `.claude/agents/<your-agent-name>.md` with this frontmatter shape:

```markdown
---
name: your-agent-name
description: What this agent checks, and when the QA Test Lead should use it.
tools: Read, Grep, Glob
model: sonnet
effort: medium
---

You are the **Your Agent Display Name**, a QA specialist focused on ...

## What to look for
- ...

## Output format

Report every finding as one row in a single markdown table with exactly these columns — do not add an "Agent" column, the orchestrator adds that:

| Severity | Issue | Impact | How to Replicate | Recommendation |
|---|---|---|---|---|

- **Severity**: exactly one of `Critical`, `High`, `Medium`, `Low`, `Informational`.
- ...

Rules:
- Do not modify any files. Do not run, build, or deploy the application.
- Only report issues you can point to in the actual code.
- If you find nothing notable, return a single `Informational` row saying so.
```

Keep the output format section identical across agents — the QA Test Lead depends on that exact 5-column table shape to merge everything into the final report.

## 2. Wire it into the QA Test Lead

Edit `.claude/agents/qa-test-lead.md`:

- Add your agent's `name` to Step 2 (if it's independent of the others) or describe its dependency explicitly like the security pair in Step 3 (if it needs another agent's output first).
- Add its display name to the list of exact Agent-column names in Step 4.

## 3. That's it

No changes needed to the HTML template or report-writing logic — those are generic over however many findings come in.
