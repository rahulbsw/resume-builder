# Resume Intelligence Foundation Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Phase 1 and Phase 2 of the Resume Intelligence roadmap without changing the current default plugin behavior.

**Architecture:** Add a small deterministic foundation under the existing workflow: a local source inventory helper, an evidence schema reference, a run summary template, warning-only quality gate guidance, and dry-run coverage. The current agent-guided `$resume-intelligence` flow remains the default; scripts and schemas assist the agent but do not replace source review, user approval, or existing outputs.

**Tech Stack:** Codex/Claude plugin metadata, Markdown skill/reference/template files, Python 3 standard library, `unittest`, official Codex plugin and skill validators, Claude plugin validators.

---

## Scope

This plan implements the first safe slice from the roadmap spec:

- Phase 1: Protect current behavior.
- Phase 2: Deterministic source and evidence helpers.

This plan does not implement the visual template profiles, career coach, interview coach, setup doctor, sample runs, disclosure approval queue, or advanced job pipeline. Those are later phases built on this foundation.

## File Structure

- Modify `README.md`: document compatibility, `run-summary.md`, and the inventory helper as optional support.
- Modify `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md`: add `run-summary.md`, the evidence schema reference, and warning-only quality gate wording.
- Modify `plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md`: add compatibility rule, run summary, and quality gate behavior.
- Modify `plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md`: document the inventory helper output contract.
- Create `plugins/resume-intelligence/skills/resume-intelligence/references/evidence-schema.md`: structured evidence JSON reference.
- Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/run-summary.md`: user-facing run summary template.
- Create `plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py`: recursive source inventory helper.
- Create `tests/resume_intelligence/test_inventory_sources.py`: unit tests for inventory behavior.
- Modify `plugins/resume-intelligence/validation/dry-run-scenarios.md`: add scenarios for compatibility, run summary, inventory helper, and evidence schema.
- Modify `plugins/resume-intelligence/.codex-plugin/plugin.json`: cachebuster only after the feature is complete.

## Task 1: Add the Source Inventory Helper Test

**Files:**
- Create: `tests/resume_intelligence/test_inventory_sources.py`

- [ ] **Step 1: Create the test directory**

Run:

```bash
mkdir -p tests/resume_intelligence
```

Expected: command exits 0.

- [ ] **Step 2: Add the failing unit tests**

Create `tests/resume_intelligence/test_inventory_sources.py` with:

```python
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "plugins"
    / "resume-intelligence"
    / "skills"
    / "resume-intelligence"
    / "scripts"
    / "inventory_sources.py"
)


def load_inventory_module():
    spec = importlib.util.spec_from_file_location("inventory_sources", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InventorySourcesTest(unittest.TestCase):
    def test_inventory_recurses_and_classifies_files(self):
        module = load_inventory_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "platform" / "architecture").mkdir(parents=True)
            (root / "platform" / "architecture" / "design.md").write_text(
                "# Design\nKubernetes migration improved deployment reliability.\n",
                encoding="utf-8",
            )
            (root / "platform" / "metadata.json").write_text(
                '{"project": "platform"}',
                encoding="utf-8",
            )
            (root / "platform" / "report.docx").write_bytes(b"PK\\x03\\x04fake-docx")
            (root / "platform" / "diagram.png").write_bytes(b"\\x89PNG\\r\\n\\x1a\\n")
            (root / "platform" / "unknown.custom").write_text("custom", encoding="utf-8")

            rows = module.inventory_root(root)
            by_path = {row.relative_path: row for row in rows}

            self.assertEqual(
                sorted(by_path),
                [
                    "platform/architecture/design.md",
                    "platform/diagram.png",
                    "platform/metadata.json",
                    "platform/report.docx",
                    "platform/unknown.custom",
                ],
            )
            self.assertEqual(by_path["platform/architecture/design.md"].status, "scanned")
            self.assertEqual(by_path["platform/metadata.json"].status, "scanned")
            self.assertEqual(by_path["platform/report.docx"].status, "needs-user-input")
            self.assertEqual(by_path["platform/diagram.png"].status, "skipped-binary")
            self.assertEqual(by_path["platform/unknown.custom"].status, "skipped-unsupported-format")

    def test_markdown_render_includes_command_and_rows(self):
        module = load_inventory_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.md").write_text("resume evidence", encoding="utf-8")

            rows = module.inventory_root(root)
            markdown = module.render_markdown(root, rows, command="inventory_sources.py")

            self.assertIn("# Source Inventory", markdown)
            self.assertIn("inventory_sources.py", markdown)
            self.assertIn("| notes.md | .md | scanned | direct-read |", markdown)
            self.assertIn("Total files: 1", markdown)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests and verify they fail because the helper does not exist**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: command exits non-zero with an error that includes:

```text
FileNotFoundError
```

- [ ] **Step 4: Commit the failing tests**

Run:

```bash
git add tests/resume_intelligence/test_inventory_sources.py
git commit -m "Add source inventory helper tests"
```

Expected: commit succeeds with only the new test file.

## Task 2: Implement the Source Inventory Helper

**Files:**
- Create: `plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py`
- Test: `tests/resume_intelligence/test_inventory_sources.py`

- [ ] **Step 1: Add the helper script**

Create `plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py` with:

```python
#!/usr/bin/env python3
"""Inventory approved local evidence folders for Resume Intelligence.

The helper only records source coverage. It does not decide final resume claims.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".adoc",
    ".csv",
    ".html",
    ".json",
    ".log",
    ".md",
    ".rst",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

DOCUMENT_EXTENSIONS = {".docx", ".pdf"}

BINARY_EXTENSIONS = {
    ".avif",
    ".bin",
    ".gif",
    ".heic",
    ".ico",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp4",
    ".pages",
    ".png",
    ".ppt",
    ".pptx",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}


@dataclass(frozen=True)
class InventoryRow:
    relative_path: str
    extension: str
    status: str
    extraction_method: str
    size_bytes: int
    modified_time: str
    notes: str


def format_mtime(path: Path) -> str:
    return str(int(path.stat().st_mtime))


def has_binary_marker(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(2048)
    except OSError:
        return False
    return b"\x00" in chunk


def classify_file(root: Path, path: Path) -> InventoryRow:
    relative_path = path.relative_to(root).as_posix()
    extension = path.suffix.lower()

    try:
        size_bytes = path.stat().st_size
        modified_time = format_mtime(path)
    except OSError as exc:
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="skipped-permission",
            extraction_method="none",
            size_bytes=0,
            modified_time="unknown",
            notes=f"stat failed: {exc.__class__.__name__}",
        )

    if extension in BINARY_EXTENSIONS or has_binary_marker(path):
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="skipped-binary",
            extraction_method="none",
            size_bytes=size_bytes,
            modified_time=modified_time,
            notes="binary or media file",
        )

    if extension in TEXT_EXTENSIONS:
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="scanned",
            extraction_method="direct-read",
            size_bytes=size_bytes,
            modified_time=modified_time,
            notes="text-oriented file ready for evidence review",
        )

    if extension in DOCUMENT_EXTENSIONS:
        return InventoryRow(
            relative_path=relative_path,
            extension=extension,
            status="needs-user-input",
            extraction_method="external-parser-required",
            size_bytes=size_bytes,
            modified_time=modified_time,
            notes="use DOCX/PDF tooling or ask user for converted text",
        )

    return InventoryRow(
        relative_path=relative_path,
        extension=extension,
        status="skipped-unsupported-format",
        extraction_method="none",
        size_bytes=size_bytes,
        modified_time=modified_time,
        notes="unsupported extension for first-pass inventory",
    )


def inventory_root(root: Path) -> list[InventoryRow]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"approved root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"approved root is not a directory: {root}")

    rows: list[InventoryRow] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            name for name in dirnames if name not in {".git", ".hg", ".svn", "__pycache__"}
        )
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            rows.append(classify_file(root, path))
    return rows


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(root: Path, rows: list[InventoryRow], command: str) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    lines = [
        "# Source Inventory",
        "",
        "## Inventory Summary",
        "",
        f"- Approved root: `{root.expanduser().resolve()}`",
        f"- Inventory command: `{command}`",
        f"- Total files: {len(rows)}",
    ]
    for status in sorted(counts):
        lines.append(f"- {status}: {counts[status]}")

    lines.extend(
        [
            "",
            "## Files",
            "",
            "| Relative Path | Extension | Status | Extraction Method | Size Bytes | Modified Time | Notes |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(row.relative_path),
                    markdown_escape(row.extension),
                    markdown_escape(row.status),
                    markdown_escape(row.extraction_method),
                    markdown_escape(row.size_bytes),
                    markdown_escape(row.modified_time),
                    markdown_escape(row.notes),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a recursive source inventory markdown file.")
    parser.add_argument("root", help="Approved local evidence folder to inventory.")
    parser.add_argument("--output", help="Markdown output path. Prints to stdout when omitted.")
    args = parser.parse_args()

    root = Path(args.root)
    command = " ".join(["inventory_sources.py", args.root] + (["--output", args.output] if args.output else []))
    rows = inventory_root(root)
    markdown = render_markdown(root, rows, command=command)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the unit tests**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: command exits 0 and includes:

```text
Ran 2 tests
OK
```

- [ ] **Step 3: Run the helper manually against the repository docs**

Run:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py docs/superpowers
```

Expected: command exits 0 and prints Markdown containing:

```text
# Source Inventory
docs/superpowers/specs/2026-05-30-resume-intelligence-design.md
```

- [ ] **Step 4: Commit the helper**

Run:

```bash
git add plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py tests/resume_intelligence/test_inventory_sources.py
git commit -m "Add deterministic source inventory helper"
```

Expected: commit succeeds with the helper and passing tests.

## Task 3: Add Evidence Schema and Run Summary Templates

**Files:**
- Create: `plugins/resume-intelligence/skills/resume-intelligence/references/evidence-schema.md`
- Create: `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/run-summary.md`

- [ ] **Step 1: Add the evidence schema reference**

Create `plugins/resume-intelligence/skills/resume-intelligence/references/evidence-schema.md` with:

````markdown
# Evidence Schema

Use this reference when a run needs structured evidence that can support resume writing, interview preparation, job scoring, redaction, and run summaries.

The Markdown `evidence.md` file remains the human-readable source. A future `evidence.json` companion may use this schema for deterministic checks.

## Evidence Object

```json
{
  "schema_version": "1.0",
  "candidate_context": {
    "target_roles": ["Staff Platform Engineer"],
    "target_seniority": "staff",
    "years_of_experience": 12,
    "location_preference": "United States remote or hybrid"
  },
  "source_contexts": [
    {
      "id": "local-docs-platform",
      "type": "local-docs",
      "display_name": "Platform project documents",
      "host": "/approved/folder",
      "identity": "user-provided",
      "credential_boundary": "local-filesystem",
      "access_method": "local file",
      "scope": "approved folder and nested files",
      "inventory_reference": "source-inventory.md",
      "tool_usage_reference": "tool-usage-log.md",
      "disclosure_level": "internal-summary-only",
      "quoting_rule": "summarize-only",
      "status": "used"
    }
  ],
  "claims": [
    {
      "id": "claim-001",
      "source_context_id": "local-docs-platform",
      "employer_or_org": "Company Name",
      "role_title": "Staff Platform Engineer",
      "date_range": "2021-2024",
      "project_or_workstream": "Platform Reliability Program",
      "user_ownership": "Led architecture and rollout",
      "responsibilities": ["Designed service health standards", "Improved deployment workflow"],
      "technologies": ["Kubernetes", "Terraform", "Observability"],
      "scale": "Multiple engineering teams",
      "impact": "Improved reliability and developer productivity",
      "metrics": [
        {
          "name": "Incident reduction",
          "value": "needs-user-input",
          "context": "User needs to provide before-and-after incident count"
        }
      ],
      "confidence": "medium",
      "disclosure_level": "internal-summary-only",
      "resume_use": "include-sanitized",
      "missing_user_question": "What measurable reliability, incident, latency, cost, or productivity change came from this work?"
    }
  ]
}
```

## Required Claim Fields

Every claim used in polished outputs should have:

- `id`
- `source_context_id`
- `project_or_workstream`
- `user_ownership`
- `technologies`
- `impact`
- `confidence`
- `disclosure_level`
- `resume_use`

## Confidence Values

- `high`: direct source evidence or user-confirmed detail.
- `medium`: supported by sources but missing a date, metric, ownership boundary, or exact scope.
- `low`: plausible but needs explicit user confirmation before polished wording.

## Resume Use Values

- `include`: safe to use directly.
- `include-sanitized`: use only with internal names, URLs, IDs, customers, or exact metrics removed.
- `needs-confirmation`: ask the user before final output.
- `exclude`: do not use in resume, LinkedIn, cover letter, or interview material.

## Quality Gate Use

Use the schema to check:

- Claims without source context.
- Medium or low confidence claims in polished outputs.
- Internal details that require sanitization.
- Metrics marked `needs-user-input`.
- Missing ownership, date, scale, or impact.
````

- [ ] **Step 2: Add the run summary template**

Create `plugins/resume-intelligence/skills/resume-intelligence/assets/templates/run-summary.md` with:

```markdown
# Run Summary

## Request

- Run goal:
- Target role or job:
- Target seniority:
- Years of experience:
- Output folder:
- Run date:

## Sources Approved

| Source Context | Type | Scope | Disclosure Rule | Status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Tools And Commands Used

| Tool / Command | Purpose | Source Context | Result |
| --- | --- | --- | --- |
|  |  |  |  |

## Source Coverage

| Source | Scanned | Skipped | Needs User Input | Notes |
| --- | ---: | ---: | ---: | --- |
|  |  |  |  |  |

## Outputs Created

| Output | Status | Notes |
| --- | --- | --- |
| `source-inventory.md` |  |  |
| `tool-usage-log.md` |  |  |
| `evidence.md` |  |  |
| `run-summary.md` |  |  |

## Warning-Only Quality Gates

| Gate | Result | Recommended Fix |
| --- | --- | --- |
| ATS safety |  |  |
| Recruiter first-page strength |  |  |
| Unsupported or weak claims |  |  |
| Keyword coverage |  |  |
| Missing metrics |  |  |
| Confidentiality and redaction risk |  |  |
| Recursive source coverage |  |  |

## Sensitive Details Awaiting Approval

| Detail Type | Source | Proposed Treatment | User Decision Needed |
| --- | --- | --- | --- |
| Internal project name |  | Sanitize |  |
| Customer name |  | Sanitize |  |
| Private repository name |  | Sanitize |  |
| Jira or Confluence identifier |  | Sanitize |  |
| Exact internal metric |  | Ask before using |  |

## Missing Information To Ask User

| Question | Why It Matters | Priority |
| --- | --- | --- |
| What exact dates apply to this role or project? | Timeline accuracy | High |
| What metric changed after this work? | Resume and interview impact | High |
| What part did you personally own? | Interview credibility | High |
| What scale was involved? | Technical depth | Medium |
| Can this name, metric, or customer detail be used publicly? | Disclosure safety | High |

## Next Actions

- 
```

- [ ] **Step 3: Commit the templates and schema**

Run:

```bash
git add plugins/resume-intelligence/skills/resume-intelligence/references/evidence-schema.md plugins/resume-intelligence/skills/resume-intelligence/assets/templates/run-summary.md
git commit -m "Add evidence schema and run summary template"
```

Expected: commit succeeds with two new Markdown files.

## Task 4: Wire the Foundation Into the Skill Workflow

**Files:**
- Modify: `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md`
- Modify: `plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md`
- Modify: `plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md`
- Modify: `README.md`

- [ ] **Step 1: Update the skill references and output list**

Patch `plugins/resume-intelligence/skills/resume-intelligence/SKILL.md`:

```diff
@@
 - Read `references/source-model.md` before collecting evidence from more than one source or any GitHub source.
+- Read `references/evidence-schema.md` before creating structured evidence, run summaries, or quality-gate checks.
@@
 - `evidence.md`
+- `run-summary.md`
@@
-1. Build `source-inventory.md` and `tool-usage-log.md` first.
+1. Build `source-inventory.md` and `tool-usage-log.md` first.
@@
-13. Create `linkedin-recommendations.md` with editable profile updates.
+13. Create `linkedin-recommendations.md` with editable profile updates.
+14. Create `run-summary.md` for substantial runs. Summarize source coverage, tools used, outputs created, warning-only quality gates, sensitive approval needs, and missing user questions.
```

- [ ] **Step 2: Add compatibility and run summary guidance**

Append this section near the top of `plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md`, after `# Resume Workflow`:

```markdown
## Compatibility Rule

Current behavior remains the default. New helpers, schemas, and quality gates assist the agent but do not replace the existing agent-guided workflow.

Do not block resume generation because a recommended helper is unavailable. Record the limitation in `tool-usage-log.md`, continue with available sources, and ask the user for missing information. Block only when output would expose credentials, secrets, private URLs, or unapproved confidential details.
```

Add this section after `## Source Inventory and Tool Log`:

````markdown
## Optional Source Inventory Helper

When available, `scripts/inventory_sources.py` can create a first-pass recursive inventory for an approved local folder:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/inventory_sources.py <approved-folder> --output resume-runs/<run>/source-inventory.md
```

Use the helper output as source coverage evidence, then continue normal evidence extraction. The helper does not decide final resume claims.
````

Add this section before `## Resume Scorecard`:

```markdown
## Run Summary

Create `run-summary.md` for substantial runs that involve more than one source, local folder inventory, job-specific tailoring, interview preparation, visual output, or enterprise/private evidence.

The run summary should show:

- User request and run goal.
- Sources approved and scanned.
- Tools and commands used.
- Files skipped and why.
- Outputs created.
- Warning-only quality gates.
- Sensitive details awaiting approval.
- Missing dates, metrics, ownership, scale, or outcomes.

The run summary is a user-facing audit and handoff artifact. It should be concise enough to read quickly.
```

In the `## Resume Scorecard` section, add this paragraph before `### Page-Length Strategy`:

```markdown
Quality gates are warning-only unless the output would expose credentials, secrets, private URLs, or unapproved confidential details. Use quality gates to make risk visible and guide user follow-up; do not silently stop the workflow because a non-critical score is weak.
```

- [ ] **Step 3: Document the helper in the source model**

Append this section to `plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md`:

```markdown
## Inventory Helper Contract

The optional local helper `scripts/inventory_sources.py` produces Markdown inventory rows with:

- Relative path.
- Extension.
- Status.
- Extraction method.
- Size in bytes.
- Modified time.
- Notes.

Statuses from the helper are first-pass coverage statuses. The agent may update `source-inventory.md` after extracting content, parsing documents with additional tools, detecting duplicates, or receiving user-provided summaries.
```

- [ ] **Step 4: Update README output and usage documentation**

Patch `README.md`:

```diff
@@
 - `evidence.md`: source-backed claims with confidence and disclosure rules.
+- `run-summary.md`: concise audit of sources scanned, tools used, outputs created, quality warnings, sensitive approvals, and missing user answers.
@@
 ## Best Practices
 
+- Treat current behavior as the default. New helpers and quality gates should improve visibility without blocking normal resume generation.
 - Keep ATS and visual outputs separate. Use `ats-resume.docx` for job portals and `designed-resume.html` or `designed-resume.pdf` for recruiter/referral sharing.
@@
 ## Optimization Tips
 
+- Use `scripts/inventory_sources.py` when you want a deterministic first-pass inventory of a local evidence folder.
 - Narrow connector queries by repo, project, space, date range, issue type, or keyword before pulling large histories.
```

- [ ] **Step 5: Commit the workflow wiring**

Run:

```bash
git add README.md plugins/resume-intelligence/skills/resume-intelligence/SKILL.md plugins/resume-intelligence/skills/resume-intelligence/references/resume-workflow.md plugins/resume-intelligence/skills/resume-intelligence/references/source-model.md
git commit -m "Wire foundation helpers into resume workflow"
```

Expected: commit succeeds with documentation-only workflow changes.

## Task 5: Add Dry-Run Scenarios for the Foundation

**Files:**
- Modify: `plugins/resume-intelligence/validation/dry-run-scenarios.md`

- [ ] **Step 1: Add compatibility and helper scenarios**

Append this content to `plugins/resume-intelligence/validation/dry-run-scenarios.md`:

```markdown
## Scenario 12: Compatibility And Warning-Only Quality Gates

Input:

- Goal: general resume and interview prep.
- Years of experience: 12.
- Sources: pasted LinkedIn profile, local documents, and public GitHub summary.
- Limitation: local inventory helper is unavailable.
- Evidence gaps: missing exact metric and one unclear ownership boundary.

Expected outputs:

- Existing outputs such as `source-inventory.md`, `tool-usage-log.md`, `evidence.md`, `draft-resume.md`, `professional-resume.md`, and interview-prep files still use the existing workflow.
- `tool-usage-log.md` records that the optional inventory helper was unavailable.
- `run-summary.md` lists the limitation and missing user questions.
- `resume-scorecard.md` treats missing metrics and weak ownership as warnings.
- Resume generation continues unless credentials, secrets, private URLs, or unapproved confidential details would be exposed.

## Scenario 13: Deterministic Local Source Inventory

Input:

- Goal: evidence extraction and detailed interview resume.
- Local root contains nested folders with Markdown, JSON, DOCX, PDF, PNG, and unsupported custom files.
- User approves the local root for inventory.

Expected outputs:

- `source-inventory.md` is produced or seeded from `scripts/inventory_sources.py`.
- Every nested file appears in the inventory.
- Text-oriented files are marked scanned for first-pass review.
- DOCX and PDF files are marked needs-user-input or later updated when document tooling extracts text.
- Binary and unsupported files are listed with reasons.
- `tool-usage-log.md` records the inventory helper command or documented fallback.
- `run-summary.md` reports total scanned, skipped, and needs-user-input files.

## Scenario 14: Evidence Schema And Run Summary

Input:

- Goal: job-specific resume and interview prep.
- Evidence contains five claims across local docs, public GitHub, and GitHub Enterprise summaries.
- Two claims are medium confidence because metrics are missing.
- One claim requires sanitized enterprise wording.

Expected outputs:

- `evidence.md` follows the evidence schema fields in human-readable Markdown.
- If `evidence.json` is created, it follows `references/evidence-schema.md`.
- `run-summary.md` lists source contexts, outputs created, warning-only quality gates, missing metrics, and sensitive approval needs.
- Final polished outputs use high-confidence and approved medium-confidence claims only.
- Low-confidence or sensitive claims remain questions or sanitized summaries.
```

- [ ] **Step 2: Commit the scenarios**

Run:

```bash
git add plugins/resume-intelligence/validation/dry-run-scenarios.md
git commit -m "Add foundation dry-run scenarios"
```

Expected: commit succeeds with validation scenario additions.

## Task 6: Validate Plugin, Cachebuster, and Local Install

**Files:**
- Modify: `plugins/resume-intelligence/.codex-plugin/plugin.json`

- [ ] **Step 1: Run Python tests**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: command exits 0 and includes:

```text
Ran 2 tests
OK
```

- [ ] **Step 2: Update the plugin cachebuster**

Run:

```bash
PYTHONPATH=/Users/rajain5/.cache/pre-commit/repo9wem9bwt/py_env-python3.13/lib/python3.13/site-packages python3 /Users/rajain5/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py plugins/resume-intelligence
```

Expected: command exits 0 and prints:

```text
Updated plugin version:
```

- [ ] **Step 3: Run Codex plugin validation**

Run:

```bash
PYTHONPATH=/Users/rajain5/.cache/pre-commit/repo9wem9bwt/py_env-python3.13/lib/python3.13/site-packages python3 /Users/rajain5/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/resume-intelligence
```

Expected: command exits 0 and prints:

```text
Plugin validation passed
```

- [ ] **Step 4: Run skill validation**

Run:

```bash
PYTHONPATH=/Users/rajain5/.cache/pre-commit/repo9wem9bwt/py_env-python3.13/lib/python3.13/site-packages python3 /Users/rajain5/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/resume-intelligence/skills/resume-intelligence
```

Expected: command exits 0 and prints:

```text
Skill is valid!
```

- [ ] **Step 5: Run Claude plugin validations**

Run:

```bash
claude plugin validate .
claude plugin validate plugins/resume-intelligence
```

Expected: both commands exit 0 and print validation passed messages.

- [ ] **Step 6: Scan for incomplete markers and whitespace issues**

Run:

```bash
rg -n "TO[D]O|TB[D]|FIX[M]E|\\[TO[D]O" README.md .claude-plugin plugins/resume-intelligence docs/superpowers tests
git diff --check
```

Expected:

- `rg` exits 1 with no matches.
- `git diff --check` exits 0 with no output.

- [ ] **Step 7: Reinstall the local Codex plugin**

Run:

```bash
codex plugin add resume-intelligence@resume-builder-local
```

Expected: command exits 0 and prints:

```text
Added plugin `resume-intelligence` from marketplace `resume-builder-local`.
```

- [ ] **Step 8: Commit cachebuster and final validation updates**

Run:

```bash
git add plugins/resume-intelligence/.codex-plugin/plugin.json
git commit -m "Validate foundation roadmap implementation"
```

Expected: commit succeeds if the cachebuster changed. If no file changed, record the validation commands in the final response and skip this commit.

## Task 7: Final Verification And Handoff

**Files:**
- Inspect only.

- [ ] **Step 1: Verify branch state**

Run:

```bash
git status --short --branch
git log --oneline -5
```

Expected:

- Status shows only the expected branch ahead count or clean working tree.
- Latest commits correspond to the completed tasks.

- [ ] **Step 2: Summarize implementation results**

Final response must include:

- Files created and modified.
- Test and validation commands run with outcomes.
- Whether the local plugin was reinstalled.
- Whether current default behavior was preserved.
- Any limitations or follow-up phases not implemented.

## Self-Review

Spec coverage:

- Compatibility rule: Task 4 updates workflow guidance and README.
- Source inventory helper: Tasks 1 and 2 add tests and script.
- Evidence normalization: Task 3 adds the schema reference.
- Run summary: Task 3 adds the template and Task 4 wires it into the workflow.
- Quality gates: Task 4 adds warning-only wording.
- Dry-run scenarios: Task 5 adds coverage.
- Validation: Task 6 lists required checks.

Out of scope by design:

- Visual template profiles.
- Career and interview coaching loop.
- Setup doctor.
- Sample fake runs.
- Enterprise disclosure approval queue.
- Advanced automation runner.

Those are later roadmap phases after this foundation slice lands.
