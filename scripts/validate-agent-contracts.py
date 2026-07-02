#!/usr/bin/env python3
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".claude" / "agents"

SPECIALISTS = [
    "api-testing-agent.md",
    "database-testing-agent.md",
    "functional-testing-agent.md",
    "gdpr-compliance-agent.md",
    "non-functional-testing-agent.md",
    "security-attack-agent.md",
    "security-defence-agent.md",
]

JSON_KEYS = [
    "id",
    "severity",
    "confidence",
    "issue",
    "impact",
    "evidence",
    "how_to_replicate",
    "recommendation",
]

SEVERITIES = ["Critical", "High", "Medium", "Low", "Informational"]
CONFIDENCES = ["High", "Medium", "Low"]


def fail(message):
    print(f"ERROR: {message}")
    return 1


def require(text, needle, path, errors):
    if needle not in text:
        errors.append(f"{path}: missing {needle!r}")


def validate_specialist(path):
    text = path.read_text(encoding="utf-8")
    errors = []

    require(text, "Return only a JSON array of finding objects", path, errors)
    require(text, ", ".join(f"`{key}`" for key in JSON_KEYS), path, errors)
    require(text, "If not dynamically tested, say `Static analysis only`", path, errors)
    if (
        "never send traffic to non-localhost targets" not in text
        and "never touch a non-localhost database" not in text
    ):
        errors.append(f"{path}: missing non-localhost safety rule")
    if "Use the Discovery Packet" not in text:
        errors.append(f"{path}: missing Discovery Packet guidance")

    for severity in SEVERITIES:
        require(text, f"`{severity}`", path, errors)
    for confidence in CONFIDENCES:
        require(text, f"`{confidence}`", path, errors)

    stale_patterns = [
        "markdown table",
        "| ID | Severity",
        "Agent column",
        "one-line summary above the table",
    ]
    for pattern in stale_patterns:
        if pattern in text:
            errors.append(f"{path}: stale table contract text {pattern!r}")

    return errors


def validate_lead(path):
    text = path.read_text(encoding="utf-8")
    errors = []

    require(text, "returns a JSON array of finding objects", path, errors)
    for key in JSON_KEYS:
        require(text, f"`{key}`", path, errors)
    require(text, "Write the same normalized report data", path, errors)
    require(text, "reports/<same-basename>.json", path, errors)
    require(text, "agents_skipped", path, errors)
    require(text, "dynamic_testing_authorized", path, errors)

    numbered = re.findall(r"^([0-9]+)\. \*\*", text, flags=re.MULTILINE)
    if numbered.count("7") > 1:
        errors.append(f"{path}: duplicate numbered merge step 7")

    return errors


def main():
    errors = []

    for name in SPECIALISTS:
        errors.extend(validate_specialist(AGENTS / name))

    errors.extend(validate_lead(AGENTS / "qa-test-lead.md"))

    docs = (ROOT / "docs" / "adding-a-new-agent.md").read_text(encoding="utf-8")
    if "Return only a JSON array of finding objects" not in docs:
        errors.append("docs/adding-a-new-agent.md: missing JSON output contract")

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("Agent contracts look consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
