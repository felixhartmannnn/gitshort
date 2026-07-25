from __future__ import annotations


def render_text(repo: object) -> str:
    root = repo.root
    branch = repo.branch
    upstream = repo.upstream
    ahead = repo.ahead
    behind = repo.behind
    dirty = repo.dirty
    staged = repo.staged
    unstaged = repo.unstaged

    lines: list[str] = [f"? {root.split('/')[-1] or root}"]
    lines.append(f"  branch: {branch or 'detached'}")
    if upstream:
        if ahead or behind:
            lines.append(f"  {upstream}: ahead {ahead} / behind {behind}")
        else:
            lines.append(f"  {upstream}: synced")
    else:
        lines.append("  upstream: n/a")
    state = "dirty" if dirty else "clean"
    lines.append(f"  changes: {state} ({staged} staged, {unstaged} unstaged)")
    return "\n".join(lines)


def render_json(repo: object) -> str:
    import json
    return json.dumps(
        {
            "root": repo.root,
            "branch": repo.branch,
            "upstream": repo.upstream,
            "ahead": repo.ahead,
            "behind": repo.behind,
            "dirty": repo.dirty,
            "staged": repo.staged,
            "unstaged": repo.unstaged,
        },
        indent=2,
    )
