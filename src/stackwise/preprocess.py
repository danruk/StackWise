"""Text preprocessing utilities for StackWise."""

import re
from typing import List


def normalize_text(text: str) -> str:
    """Normalize raw Stack Overflow text for downstream NLP tasks."""
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    """Simple tokenization for source code and text snippets."""
    normalized = normalize_text(text)
    return re.findall(r"[a-z0-9_]+", normalized)
