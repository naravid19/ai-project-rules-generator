import unittest
from scripts.lib.semantic_matcher import SemanticMatcher

class TestSemanticMatcher(unittest.TestCase):
    def test_synonym_matching(self):
        matcher = SemanticMatcher()
        # "security" should match "auth" via synonyms
        score = matcher.score("auth", ["security", "react"])
        self.assertGreater(score, 0)
        
    def test_fuzzy_matching(self):
        matcher = SemanticMatcher()
        # "frontend" should match "front-end" fuzzy
        score = matcher.score("frontend", ["front-end"])
        self.assertGreater(score, 0.8)

if __name__ == "__main__":
    unittest.main()
