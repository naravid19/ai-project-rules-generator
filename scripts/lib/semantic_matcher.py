from __future__ import annotations
import difflib
from typing import Sequence

SYNONYMS = {
    "auth": ["security", "login", "identity", "oauth", "jwt", "authentication", "authorization"],
    "api": ["backend", "rest", "graphql", "interface", "endpoint", "route", "server"],
    "frontend": ["ui", "ux", "react", "vue", "web", "component", "layout", "page"],
    "test": ["pytest", "jest", "quality", "vitest", "unit", "e2e", "integration", "coverage"],
    "database": ["sql", "postgres", "mysql", "mongodb", "orm", "migration", "schema", "prisma"],
    "deploy": ["docker", "kubernetes", "k8s", "ci", "cd", "pipeline", "infra", "cloud"],
    "ai": ["ml", "llm", "model", "training", "inference", "embedding", "rag", "agent"],
    "mobile": ["ios", "android", "flutter", "react-native", "swift", "kotlin"],
    "state": ["redux", "zustand", "mobx", "store", "context", "signal"],
    "style": ["css", "tailwind", "sass", "scss", "design", "theme", "token"],
    "monitor": ["logging", "metrics", "observability", "tracing", "alert", "apm"],
    "perf": ["performance", "optimization", "cache", "lazy", "bundle", "lighthouse"],
}

class SemanticMatcher:
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def score(self, query: str, tags: Sequence[str]) -> float:
        query_tokens = query.lower().split()
        best_score = 0.0
        
        for tag in tags:
            tag_lower = tag.lower()
            for token in query_tokens:
                # 1. Literal match
                if token == tag_lower:
                    best_score = max(best_score, 1.0)
                
                # 2. Synonym match
                for base, syns in SYNONYMS.items():
                    if (token == base and tag_lower in syns) or (tag_lower == base and token in syns):
                        best_score = max(best_score, 0.9)
                
                # 3. Fuzzy match
                ratio = difflib.SequenceMatcher(None, token, tag_lower).ratio()
                if ratio >= self.threshold:
                    best_score = max(best_score, ratio)
                    
        return best_score
