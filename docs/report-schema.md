# Report schema

Each assessment writes a human-readable HTML report and a machine-readable JSON report with the same basename.

```json
{
  "app_name": "Example App",
  "app_path": "/absolute/path/to/app",
  "report_date": "2 July 2026",
  "dynamic_testing_authorized": false,
  "discovery_packet": {
    "app_name": "Example App",
    "target_path": "/absolute/path/to/app",
    "dynamic_testing_authorized": false,
    "stack": ["Node.js", "Express"],
    "entrypoints": ["src/server.js"],
    "surfaces": ["API", "database", "auth"],
    "key_paths": ["src/routes", "src/models", "migrations"],
    "available_specs": ["README.md"],
    "skip_hints": []
  },
  "agents_run": ["API Testing Agent", "Security Attack Agent"],
  "agents_skipped": [
    {
      "agent": "GDPR and Compliance Agent",
      "reason": "No personal-data flow was detected in the Discovery Packet."
    }
  ],
  "summary_counts": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0,
    "informational": 0,
    "total": 3
  },
  "exec_summary": "Short plain-English summary of the assessment.",
  "findings": [
    {
      "id": "api-users-missing-auth",
      "severity": "High",
      "confidence": "High",
      "agents": ["API Testing Agent", "Security Attack Agent"],
      "issue": "POST /users does not require authentication.",
      "impact": "An unauthenticated user can create accounts without approval.",
      "evidence": "Static analysis only — route at src/routes/users.js:22 lacks auth middleware.",
      "how_to_replicate": "1. Open the app locally. 2. Submit the create-user flow without signing in. 3. Confirm the user is created.",
      "recommendation": "Require authentication and authorization middleware before the handler."
    }
  ]
}
```

Required finding values:

- `id`: stable kebab-case identifier based on category, location, and root cause.
- `severity`: one of `Critical`, `High`, `Medium`, `Low`, `Informational`.
- `confidence`: one of `High`, `Medium`, `Low`.
- `agents`: one or more specialist display names.
- `issue`, `impact`, `evidence`, `how_to_replicate`, `recommendation`: non-empty strings.

JSON values must not contain HTML markup. The HTML report is rendered from this normalized data.
