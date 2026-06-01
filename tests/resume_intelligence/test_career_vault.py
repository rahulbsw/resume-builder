import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_ROOT = (
    Path(__file__).resolve().parents[2]
    / "plugins"
    / "resume-intelligence"
    / "skills"
    / "resume-intelligence"
    / "scripts"
)


def load_script(script_name):
    script_path = SCRIPT_ROOT / script_name
    module_name = script_name.removesuffix(".py")
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class CareerVaultBuilderTest(unittest.TestCase):
    def test_build_vault_creates_obsidian_pages_from_evidence_json(self):
        module = load_script("build_career_vault.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_json = root / "evidence.json"
            evidence_json.write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "claim": "Led Kubernetes platform modernization.",
                                "project": "Platform Modernization",
                                "technologies": ["Kubernetes", "Terraform"],
                                "source_context_id": "github-enterprise-platform",
                                "evidence_reference": "PR 123",
                                "confidence": "high",
                                "disclosure_level": "internal-summary-only",
                                "resume_use": "include-sanitized",
                            },
                            {
                                "claim": "Maintained public SDK releases.",
                                "project": "Open Source SDK",
                                "technologies": ["Python"],
                                "source_context_id": "github-public-sdk",
                                "evidence_reference": "release v1.2",
                                "confidence": "medium",
                                "disclosure_level": "public",
                                "resume_use": "include",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            vault = module.build_vault(
                evidence_path=evidence_json,
                output_dir=root / "career-vault",
                run_name="Staff Platform Engineer",
                run_date="2026-06-01",
            )

            self.assertEqual(vault.name, "career-vault")
            self.assertTrue((vault / "AGENTS.md").exists())
            self.assertTrue((vault / "index.md").exists())
            self.assertTrue((vault / "log.md").exists())

            project_page = vault / "projects" / "platform-modernization.md"
            self.assertTrue(project_page.exists())
            project_text = project_page.read_text(encoding="utf-8")
            self.assertIn("tags: [project, resume-intelligence]", project_text)
            self.assertIn("[[technologies/kubernetes|Kubernetes]]", project_text)
            self.assertIn("github-enterprise-platform", project_text)
            self.assertIn("include-sanitized", project_text)

            tech_page = vault / "technologies" / "kubernetes.md"
            self.assertIn("[[projects/platform-modernization|Platform Modernization]]", tech_page.read_text(encoding="utf-8"))

            disclosure_page = vault / "disclosure" / "approval-needed.md"
            self.assertIn("Platform Modernization", disclosure_page.read_text(encoding="utf-8"))
            self.assertIn("internal-summary-only", disclosure_page.read_text(encoding="utf-8"))

            index_text = (vault / "index.md").read_text(encoding="utf-8")
            self.assertIn("[[projects/platform-modernization|Platform Modernization]]", index_text)
            self.assertIn("[[technologies/kubernetes|Kubernetes]]", index_text)

    def test_group_records_uses_uncategorized_project_when_missing(self):
        module = load_script("build_career_vault.py")
        records = [{"claim": "Improved release automation."}]

        grouped = module.group_records_by_project(records)

        self.assertEqual(list(grouped), ["Uncategorized Evidence"])


class CareerVaultLintTest(unittest.TestCase):
    def test_lint_reports_missing_evidence_links_and_orphans(self):
        module = load_script("vault_lint.py")

        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "projects").mkdir()
            (vault / "index.md").write_text("# Career Knowledge Vault Index\n", encoding="utf-8")
            (vault / "projects" / "orphan.md").write_text(
                "# Orphan Project\n\nNo evidence section here.\n", encoding="utf-8"
            )

            report = module.lint_vault(vault)

            self.assertFalse(report.ok)
            issue_text = "\n".join(issue.message for issue in report.issues)
            self.assertIn("not linked from index.md", issue_text)
            self.assertIn("missing an Evidence Links section", issue_text)

    def test_lint_passes_builder_output(self):
        builder = load_script("build_career_vault.py")
        linter = load_script("vault_lint.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence_json = root / "evidence.json"
            evidence_json.write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "claim": "Built Python automation.",
                                "project": "Automation Platform",
                                "technologies": ["Python"],
                                "source_context_id": "local-docs",
                                "evidence_reference": "notes.md",
                                "confidence": "high",
                                "disclosure_level": "public",
                                "resume_use": "include",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            vault = builder.build_vault(
                evidence_path=evidence_json,
                output_dir=root / "career-vault",
                run_name="Automation Engineer",
                run_date="2026-06-01",
            )

            report = linter.lint_vault(vault)

            self.assertTrue(report.ok, [issue.message for issue in report.issues])


if __name__ == "__main__":
    unittest.main()
