"""Recapture fingerprints from main-branch templates (no JSON-LD injection)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    Path("app/templates/base.html"),
    Path("app/templates/components/service-faq.html"),
    Path("app/templates/pages/faq.html"),
    Path("app/__init__.py"),
]


def main() -> None:
    backups: dict[Path, Path] = {}
    for path in FILES:
        backup = ROOT / path.with_suffix(path.suffix + ".bak")
        shutil.copy2(ROOT / path, backup)
        backups[path] = backup

    try:
        subprocess.run(
            ["git", "checkout", "main", "--", *[str(p) for p in FILES]],
            check=True,
            cwd=ROOT,
        )
        import os

        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT)
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "capture_html_fingerprints.py")],
            check=True,
            cwd=ROOT,
            env=env,
        )
    finally:
        for path, backup in backups.items():
            shutil.copy2(backup, ROOT / path)
            backup.unlink(missing_ok=True)
        print("restored feature-branch files")


if __name__ == "__main__":
    main()
