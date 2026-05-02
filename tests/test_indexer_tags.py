import unittest
from scripts.indexer import _extract_tags
from pathlib import Path

class TestTagExtraction(unittest.TestCase):
    def test_extract_tags_exact_match(self):
        description = "A skill to interact with the capitalism api"
        content = "This skill uses apis."
        path = Path("skills/capitalism-skill/SKILL.md")
        
        # 'api' is a tag, but 'capitalism' contains 'api'. It shouldn't match.
        tags = _extract_tags(description, content, path)
        self.assertIn("api", tags)
        
    def test_extract_tags_no_false_positives(self):
        description = "This skill handles reactivities and nextjstools"
        content = "It is very tailwindy."
        path = Path("skills/misc/SKILL.md")
        
        # 'react', 'nextjs', 'tailwind' are tags, but they are embedded inside other words.
        tags = _extract_tags(description, content, path)
        self.assertNotIn("react", tags)
        self.assertNotIn("nextjs", tags)
        self.assertNotIn("tailwind", tags)
