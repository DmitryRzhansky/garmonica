"""Capture content fingerprints for all public HTML pages (JSON-LD stripped)."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from app.services.catalog import get_catalog
from app.services.info_pages import INFO_PAGES

LD_RE = re.compile(
    r"\s*<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>.*?</script>",
    re.DOTALL | re.IGNORECASE,
)


def strip_ld(html: str) -> str:
    return LD_RE.sub("", html)


def public_urls() -> list[str]:
    return ["/"] + [f"/{slug}/" for slug in INFO_PAGES] + get_catalog().public_urls()


def main() -> None:
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    urls = public_urls()
    fingerprints: dict[str, dict] = {}
    status_counts: Counter[int] = Counter()
    errors: list[tuple[str, int]] = []

    for index, url in enumerate(urls, 1):
        response = client.get(url)
        status_counts[response.status_code] += 1
        if response.status_code != 200:
            errors.append((url, response.status_code))
            continue
        html = response.get_data(as_text=True)
        stripped = strip_ld(html)
        fingerprints[url] = {
            "sha256": hashlib.sha256(stripped.encode("utf-8")).hexdigest(),
            "len": len(stripped),
            "had_ldjson": bool(LD_RE.search(html)),
        }
        if index % 200 == 0:
            print(f"processed {index}/{len(urls)}", flush=True)

    out = ROOT / "tests" / "fixtures" / "html_content_fingerprints.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "count": len(fingerprints),
        "total_urls": len(urls),
        "status_counts": {str(k): v for k, v in sorted(status_counts.items())},
        "errors": errors,
        "urls": fingerprints,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"written {out} entries={len(fingerprints)} errors={len(errors)}")


if __name__ == "__main__":
    main()
