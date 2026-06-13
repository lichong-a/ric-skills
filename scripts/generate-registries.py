#!/usr/bin/env python3
"""Generate deterministic registries from skills/catalog.json."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


def parse_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^description:\s*[\"']?(.*?)[\"']?\s*$", text, re.MULTILINE)
    return match.group(1) if match else ""


def outputs(root: Path) -> dict[Path, str]:
    catalog = json.loads((root / "skills" / "catalog.json").read_text(encoding="utf-8"))
    names = sorted(catalog["skills"])
    ps_lines = ["$Skills = @{"]
    sh_lines = ["#!/usr/bin/env bash", "", "declare -A SKILLS=("]
    llms: list[str] = []
    for name in names:
        path = f"skills/{name}/SKILL.md"
        ps_lines.append(f'  "{name}" = "{path}"')
        sh_lines.append(f'  [{name}]="{path}"')
        llms.append(f"{name}: {catalog['skills'][name]['description']}")
    ps_lines += [
        "}",
        "",
        'if ($args.Count -eq 0) {',
        '  Write-Output "Usage: .\\skill.ps1 <skill-name>"',
        '  $Skills.Keys | Sort-Object | ForEach-Object { Write-Output "  $_" }',
        "  exit 0",
        "}",
        "$Name = $args[0]",
        "if ($Skills.ContainsKey($Name)) { Write-Output $Skills[$Name]; exit 0 }",
        'Write-Error "Unknown skill: $Name"',
        "exit 1",
        "",
    ]
    sh_lines += [
        ")",
        "",
        'if [[ $# -eq 0 ]]; then printf "  %s\\n" "${!SKILLS[@]}" | sort; exit 0; fi',
        'if [[ -n "${SKILLS[$1]}" ]]; then echo "${SKILLS[$1]}"; exit 0; fi',
        'echo "Unknown skill: $1" >&2',
        "exit 1",
        "",
    ]
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    begin = "<!-- BEGIN GENERATED SKILLS -->"
    end = "<!-- END GENERATED SKILLS -->"
    table = [
        begin,
        "",
        "| Install name | Default role | Trigger |",
        "| --- | --- | --- |",
    ]
    for name in names:
        entry = catalog["skills"][name]
        table.append(f"| `{name}` | {entry['default_role']} | {entry['description']} |")
    table += ["", end]
    if begin not in readme or end not in readme:
        raise ValueError("README.md must contain generated skill table markers")
    generated_readme = readme[: readme.index(begin)] + "\n".join(table) + readme[readme.index(end) + len(end) :]
    return {
        root / "skill.ps1": "\n".join(ps_lines),
        root / "skill.sh": "\n".join(sh_lines),
        root / "skills" / "llms.txt": "\n".join(llms) + "\n",
        readme_path: generated_readme,
    }


def safe_write(root: Path, path: Path, content: str) -> None:
    resolved_root = root.resolve()
    try:
        path.parent.resolve().relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"registry output parent escapes repository root: {path}") from exc
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        raise ValueError(f"refusing to write registry through link or junction: {path}")
    if path.exists():
        try:
            path.resolve().relative_to(resolved_root)
        except ValueError as exc:
            raise ValueError(f"registry output escapes repository root: {path}") from exc
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError(f"registry output became a link or junction: {path}")
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    mismatches: list[str] = []
    for path, expected in outputs(root).items():
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError(f"refusing registry output link or junction: {path}")
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if actual != expected:
            mismatches.append(path.relative_to(root).as_posix())
            if not args.check:
                safe_write(root, path, expected)
    if mismatches:
        print(("Out of date: " if args.check else "Generated: ") + ", ".join(mismatches))
    return 1 if args.check and mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
