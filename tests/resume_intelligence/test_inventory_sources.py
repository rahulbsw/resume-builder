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
