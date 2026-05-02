import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.lib.design_tokens import DesignTokenEngine

class TestDesignTokenEngine(unittest.TestCase):
    def test_engine_initialization(self):
        engine = DesignTokenEngine(Path("."))
        self.assertIsNotNone(engine)
        self.assertEqual(engine.project_root, Path("."))

    def test_structured_css_parsing(self):
        css_content = """
        :root {
            --primary-color: #ff0000;
            --font-main: 'Inter', sans-serif;
            --spacing-unit: 1rem;
        }
        """
        engine = DesignTokenEngine(Path("."))
        tokens = engine._parse_css_content(css_content)
        self.assertEqual(tokens["colors"]["--primary-color"], "#ff0000")
        self.assertEqual(tokens["fonts"]["--font-main"], "'Inter', sans-serif")
        self.assertEqual(tokens["spacing"]["--spacing-unit"], "1rem")

    @patch('subprocess.run')
    def test_tailwind_node_parsing(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout='{"theme":{"colors":{"brand":"#00ff00"}}}',
            returncode=0
        )
        engine = DesignTokenEngine(Path("."))
        # Simulate a path that exists for the method check
        config_path = Path("tailwind.config.js")
        with patch.object(Path, 'exists', return_value=True):
            tokens = engine._extract_tailwind_via_node(config_path)
        self.assertEqual(tokens["colors"]["brand"], "#00ff00")

if __name__ == "__main__":
    unittest.main()
