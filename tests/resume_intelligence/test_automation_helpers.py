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


class SetupDoctorTest(unittest.TestCase):
    def test_check_required_paths_reports_missing_files(self):
        module = load_script("setup_doctor.py")

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "plugins/resume-intelligence/skills/resume-intelligence").mkdir(
                parents=True
            )
            (repo / "plugins/resume-intelligence/skills/resume-intelligence/SKILL.md").write_text(
                "# Skill\n", encoding="utf-8"
            )

            results = module.check_required_paths(repo)
            by_name = {result.name: result for result in results}

            self.assertEqual(by_name["skill file"].status, "ok")
            self.assertEqual(by_name["codex plugin manifest"].status, "missing")

    def test_check_commands_uses_injected_resolver(self):
        module = load_script("setup_doctor.py")

        def fake_which(command):
            return f"/usr/bin/{command}" if command == "git" else None

        results = module.check_commands(["git", "soffice"], which=fake_which)
        by_name = {result.name: result for result in results}

        self.assertEqual(by_name["git"].status, "ok")
        self.assertEqual(by_name["soffice"].status, "missing")


class ResumeRunnerTest(unittest.TestCase):
    def test_create_run_folder_copies_selected_templates(self):
        module = load_script("resume_runner.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            templates = root / "templates"
            output_root = root / "resume-runs"
            templates.mkdir()
            (templates / "source-inventory.md").write_text("# Source Inventory\n", encoding="utf-8")
            (templates / "run-summary.md").write_text("# Run Summary\n", encoding="utf-8")

            run_dir = module.create_run_folder(
                output_root=output_root,
                templates_dir=templates,
                slug="Staff Platform Engineer",
                template_names=["source-inventory.md", "run-summary.md"],
                date="2026-06-01",
            )

            self.assertEqual(run_dir.name, "2026-06-01-staff-platform-engineer")
            self.assertTrue((run_dir / "source-inventory.md").exists())
            self.assertTrue((run_dir / "run-summary.md").exists())
            self.assertIn("Resume Intelligence Run", (run_dir / "README.md").read_text(encoding="utf-8"))


class EvidenceNormalizerTest(unittest.TestCase):
    def test_render_markdown_groups_claims_by_source_context(self):
        module = load_script("evidence_normalizer.py")
        records = [
            {
                "claim": "Led Kubernetes migration",
                "source_context_id": "github-enterprise-platform",
                "evidence_reference": "PR 123",
                "confidence": "high",
                "disclosure_level": "internal-summary-only",
                "resume_use": "include-sanitized",
            },
            {
                "claim": "Maintained open-source SDK",
                "source_context_id": "github-public-sdk",
                "evidence_reference": "release v1.2",
                "confidence": "medium",
                "disclosure_level": "public",
                "resume_use": "include",
            },
        ]

        markdown = module.render_markdown(records)

        self.assertIn("## github-enterprise-platform", markdown)
        self.assertIn("| Led Kubernetes migration | PR 123 | high | internal-summary-only | include-sanitized |", markdown)
        self.assertIn("## github-public-sdk", markdown)

    def test_load_records_accepts_top_level_records_key(self):
        module = load_script("evidence_normalizer.py")

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.json"
            path.write_text(json.dumps({"records": [{"claim": "Built platform"}]}), encoding="utf-8")

            self.assertEqual(module.load_records(path), [{"claim": "Built platform"}])


class ScorecardCheckerTest(unittest.TestCase):
    def test_check_scorecard_text_reports_missing_required_sections(self):
        module = load_script("scorecard_checker.py")
        markdown = "# Resume Scorecard\n\n## Recommendation\n\n## ATS Safety\n"

        result = module.check_scorecard_text(markdown)

        self.assertFalse(result.ok)
        self.assertIn("Keyword Coverage", result.missing_sections)
        self.assertIn("Recruiter First-Page Strength", result.missing_sections)

    def test_check_scorecard_text_passes_complete_scorecard(self):
        module = load_script("scorecard_checker.py")
        markdown = "\n".join(
            [
                "# Resume Scorecard",
                "## Recommendation",
                "## Page-Length Strategy",
                "## ATS Safety",
                "## Recruiter First-Page Strength",
                "## Keyword Coverage",
                "## Top Fixes Before Applying",
                "## Unsupported or Risky Claims",
                "## Detailed Resume Gaps",
                "## Final Notes",
            ]
        )

        result = module.check_scorecard_text(markdown)

        self.assertTrue(result.ok)
        self.assertEqual(result.missing_sections, [])


if __name__ == "__main__":
    unittest.main()
