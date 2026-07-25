from __future__ import annotations

import argparse
import sys
from gitshort import discover_repo, render_text, render_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gitshort",
        description="Compact git repository status snapshot.",
    )
    parser.add_argument("path", nargs="?", default=".", help="repository path")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--no-upstream", action="store_true", help="skip upstream")
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    repo = discover_repo(args.path)
    if not repo:
        print(f"error: not a git repository: {args.path}", file=sys.stderr)
        return 2
    if args.json:
        print(render_json(repo))
    else:
        print(render_text(repo))
    return 1 if repo.dirty else 0
