# Adding a new specialist QA agent

The system is designed so a new specialist is one new file plus orchestration wiring in the QA Test Lead.

## 1. Create the agent file

Add `.claude/agents/<your-agent-name>.md` with this frontmatter shape:

```markdown
---
name: your-agent-name
description: What this agent checks, and when the QA Test Lead should use it.
tools: Read, Grep, Glob, Bash
model: sonnet
effort: medium
---

You are the **Your Agent Display Name**, a QA specialist focused on ...

## What to look for
- ...

## Output format

Return only a JSON array of finding objects. Do not wrap it in markdown fences and do not add prose outside the JSON. Each object must use exactly these keys:

`id`, `severity`, `confidence`, `issue`, `impact`, `evidence`, `how_to_replicate`, `recommendation`

- **ID**: stable kebab-case identifier based on category, location, and root cause.
- **Severity**: exactly one of `Critical`, `High`, `Medium`, `Low`, `Informational`.
- **Confidence**: exactly one of `High`, `Medium`, `Low`.
- **Issue**: one clear sentence naming the problem and its location.
- **Impact**: how this affects users, quality, security, compliance, or operations.
- **Evidence**: what you directly observed, with exact files/lines for static findings or concrete local test output for dynamic findings.
- **How to Replicate**: numbered steps a reader can follow to confirm the issue.
- **Recommendation**: a specific, actionable fix.
- ...

Rules:
- Do not modify any files. Do not run, build, deploy, or send requests unless dynamic testing was explicitly authorized in the prompt.
- When dynamic testing is authorized, use local/isolated execution only and never send traffic to non-localhost targets.
- Only report issues you can point to in the actual code.
- If you find nothing notable, return a single `Informational` row saying so.
```

Keep the output format section identical across agents — the QA Test Lead depends on that exact JSON shape to merge everything into the final report.

## 2. Wire it into the QA Test Lead

Edit `.claude/agents/qa-test-lead.md`:

- Add your agent's routing rule to Step 2 (if it's independent of the others) or describe its dependency explicitly like the security pair in Step 3 (if it needs another agent's output first).
- Add its display name to the list of exact Agent-column names in Step 4.
- Update the Discovery Packet or skip/routing guidance if your agent needs a new surface signal.

## 3. That's it

No changes needed to the HTML template or report-writing logic unless your agent needs a new report field.
