import unittest
import tempfile
from pathlib import Path
from scripts.indexer import build_skill_catalog, validate_catalog

class TestIndexerJSON(unittest.TestCase):
    def test_invalid_json_logs_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            catalog_path = project_root / ".agent" / "memory" / "skill_catalog.json"
            catalog_path.parent.mkdir(parents=True)
            # Write malformed JSON
            catalog_path.write_text("{invalid_json: true")
            
            # This shouldn't crash, but it should log a warning or print to console
            # We will patch print or logger to assert it was called
            from unittest.mock import patch
            with patch('builtins.print') as mock_print:
                # Need to mock resolve_confirmed_skill_source
                with patch('scripts.indexer.resolve_confirmed_skill_source') as mock_resolve:
                    from scripts.project_rules_runtime import ConfirmedSkillSource
                    mock_resolve.return_value = ConfirmedSkillSource(
                        configured_path="skills",
                        resolved_path=project_root / "skills"
                    )
                    build_skill_catalog(project_root, output_path=catalog_path, incremental=True)
                    mock_print.assert_called()
                    call_arg = mock_print.call_args[0][0]
                    self.assertTrue(call_arg.startswith(f"Warning: Failed to parse existing catalog JSON at {catalog_path}"))
