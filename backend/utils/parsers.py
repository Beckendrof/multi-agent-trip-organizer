"""File-parsing and LLM-output-parsing helpers."""

from __future__ import annotations

import json
import os
import re

from PIL import Image

HAS_TESSERACT = True
try:
    import pytesseract
except ImportError:
    HAS_TESSERACT = False


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_image(path: str) -> str:
    """Run OCR on a receipt image and return the extracted text."""
    if not HAS_TESSERACT:
        return f"[OCR unavailable – raw file: {os.path.basename(path)}]"
    img = Image.open(path)
    return pytesseract.image_to_string(img)


def parse_llm_json(text: str) -> dict:
    """Robustly extract a JSON object from LLM output that may contain
    markdown fences, preamble text, or trailing commentary."""
    cleaned = text.strip()

    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    brace_start = cleaned.find("{")
    if brace_start == -1:
        raise ValueError(f"No JSON object found in LLM output: {text[:200]}")

    depth = 0
    for i in range(brace_start, len(cleaned)):
        if cleaned[i] == "{":
            depth += 1
        elif cleaned[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(cleaned[brace_start : i + 1])

    return json.loads(cleaned[brace_start:])
