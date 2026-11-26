"""Lightweight FAQ matcher: character n-gram TF-IDF + cosine similarity.

Character n-grams make matching tolerant to typos and to Roman-Urdu spelling
variations ("kitna" / "kitnaa"), without needing a heavy ML model.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

URDU_RANGE = re.compile(r"[؀-ۿ]")
ROMAN_URDU_HINTS = {"kya", "kitna", "kitni", "hai", "hain", "mein", "nahi", "batao", "karna", "chahiye"}


FALLBACK_ANSWER = (
    "I'm not sure about that yet. A team member will follow up - "
    "could you share your question in a bit more detail?"
)


def normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", " ", text.lower()).strip()


def ngrams(text: str, n_min: int = 2, n_max: int = 4) -> list[str]:
    out = []
    for word in normalize(text).split():
        padded = f" {word} "
        for n in range(n_min, n_max + 1):
            out += [padded[i : i + n] for i in range(len(padded) - n + 1)]
    return out


def detect_language(text: str) -> str:
    if URDU_RANGE.search(text):
        return "urdu"
    if set(normalize(text).split()) & ROMAN_URDU_HINTS:
        return "roman-urdu"
    return "english"


class FaqMatcher:
    def __init__(self, entries: list[dict], threshold: float = 0.28):
        self.entries = entries
        self.threshold = threshold
        self.docs: list[tuple[int, Counter]] = []
        df: Counter = Counter()
        for idx, e in enumerate(entries):
            for pattern in e["patterns"]:
                grams = Counter(ngrams(pattern))
                self.docs.append((idx, grams))
                df.update(grams.keys())
        n = len(self.docs)
        self.idf = {g: math.log((1 + n) / (1 + c)) + 1 for g, c in df.items()}
        self.vectors = [(i, self._vec(c)) for i, c in self.docs]

    def _vec(self, counts: Counter) -> dict[str, float]:
        v = {g: tf * self.idf.get(g, 0.0) for g, tf in counts.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {g: x / norm for g, x in v.items()}

    def match(self, query: str) -> tuple[dict | None, float]:
        q = self._vec(Counter(ngrams(query)))
        best_idx, best = None, 0.0
        for idx, vec in self.vectors:
            score = sum(w * vec.get(g, 0.0) for g, w in q.items())
            if score > best:
                best_idx, best = idx, score
        if best_idx is None or best < self.threshold:
            return None, best
        return self.entries[best_idx], best

    def reply(self, query: str) -> dict:
        entry, score = self.match(query)
        lang = detect_language(query)
        if entry is None:
            return {"answer": FALLBACK_ANSWER, "intent": "fallback", "confidence": round(score, 2), "language": lang}
        return {"answer": entry["answer"], "intent": entry["intent"], "confidence": round(score, 2), "language": lang}


def load(path: str | Path | None = None) -> FaqMatcher:
    path = Path(path) if path else Path(__file__).parent / "sample_faq.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return FaqMatcher(data["entries"])
