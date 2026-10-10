"""Safe JSON-LD serialization for embedding in HTML."""

from __future__ import annotations

import json
from typing import Any


def dumps_json_ld(data: dict[str, Any]) -> str:
    """Serialize JSON-LD and escape sequences unsafe inside HTML script tags."""
    # Default separators keep a space after ":" so existing FAQ assertions match.
    text = json.dumps(data, ensure_ascii=False)
    return (
        text.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def prune_empty(value: Any) -> Any:
    """Drop None / empty containers so incomplete data never emits empty fields."""
    if value is None:
        return None
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            pruned = prune_empty(item)
            if pruned is None:
                continue
            if pruned == "" or pruned == [] or pruned == {}:
                continue
            cleaned[key] = pruned
        return cleaned or None
    if isinstance(value, list):
        cleaned_list = []
        for item in value:
            pruned = prune_empty(item)
            if pruned is None:
                continue
            if pruned == "" or pruned == [] or pruned == {}:
                continue
            cleaned_list.append(pruned)
        return cleaned_list or None
    return value
