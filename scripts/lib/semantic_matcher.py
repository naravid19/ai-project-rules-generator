from __future__ import annotations
import difflib
from typing import Sequence

SYNONYMS = {
    "auth": ["security", "login", "identity", "oauth", "jwt"],
    "api": ["backend", "rest", "graphql", "interface"],
    "frontend": ["ui", "ux", "react", "vue", "web"],
    "test": ["pytest", "jest", "quality", "vitest", "unit"],
}

class SemanticMatcher:
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def score(self, query: str, tags: Sequence[str]) -> float:
        query = query.lower()
        best_score = 0.0
        
        for tag in tags:
            tag = tag.lower()
            # 1. Literal match
            if query == tag:
                return 1.0
            
            # 2. Synonym match
            for base, syns in SYNONYMS.items():
                if (query == base and tag in syns) or (tag == base and query in syns):
                    best_score = max(best_score, 0.9)
            
            # 3. Fuzzy match
            ratio = difflib.SequenceMatcher(None, query, tag).ratio()
            if ratio >= self.threshold:
                best_score = max(best_score, ratio)
                
        return best_score
