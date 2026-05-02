import unittest
from scripts.indexer import _collect_catalog_entries
from pathlib import Path
from unittest.mock import patch, MagicMock

class TestParallelCollection(unittest.TestCase):
    @patch('scripts.indexer.resolve_skill_entry')
    @patch('scripts.indexer._iter_entrypoints')
    def test_collect_uses_threadpool(self, mock_iter, mock_resolve):
        # Setup mocks
        mock_iter.return_value = [Path("fake/path1"), Path("fake/path2")]
        
        with patch('concurrent.futures.ThreadPoolExecutor') as mock_executor:
            # We don't actually care about the return value for this test, 
            # just that ThreadPoolExecutor is instantiated and used.
            mock_executor.return_value.__enter__.return_value.map.return_value = []
            _collect_catalog_entries(Path("."), Path("."), None)
            mock_executor.assert_called_once()
