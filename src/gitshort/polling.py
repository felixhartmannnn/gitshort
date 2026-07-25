from __future__ import annotations

import os
import subprocess
from typing import Dict, List, Optional, Sequence


class SubprocessError(RuntimeError):
    pass


def run(
    args: Sequence[str],
    *,
    cwd: str,
    check: bool = True,
    env: Optional[dict] = None,
) -> str:
    cmd = list(args)
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env or os.environ,
        )
    except FileNotFoundError as exc:
        raise SubprocessError(f"command not found: {cmd[0]}\n") from exc
    except NotADirectoryError as exc:
        raise SubprocessError(f"invalid cwd for command: {cwd}\n") from exc
    if check and result.returncode != 0:
        stderr = result.stderr.decode("utf-8", "replace")
        stdout = result.stdout.decode("utf-8", "replace")
        raise SubprocessError(
            f"command failed: {' '.join(cmd)}\nrc={result.returncode}\nstdout={stdout}\nstderr={stderr}\n"
        ) from None
    return result.stdout.decode("utf-8")


def repo_root(cwd: str) -> Optional[str]:
    try:
        return run(["git", "rev-parse", "--show-toplevel"], cwd=cwd).strip() or None
    except SubprocessError:
        return None


def current_branch(cwd: str) -> Optional[str]:
    try:
        out = run(["git", "symbolic-ref", "--quiet", "--short", "HEAD"], cwd=cwd).strip()
    except SubprocessError:
        return None
    return out or None


def upstream_branch(branch: Optional[str], cwd: str) -> Optional[str]:
    if not branch:
        return None
    ref = f"refs/remotes/*/{branch}"
    try:
        out = run(["git", "branch", "-r", "--format=%(refname:short)"], cwd=cwd)
    except SubprocessError:
        return None
    matches = [line.strip() for line in out.splitlines() if line.strip() == f"origin/{branch}"]
    return f"origin/{branch}" if matches else None


def ahead_behind(cwd: str, branch: str) -> Dict[str, int]:
    try:
        out = run(
            ["git", "rev-list", "--left-right", "--count", f"origin/{branch}...{branch}"],
            cwd=cwd,
        ).strip()
        parts = out.split("\t", 1)
        if len(parts) == 2 and "".join(filter(str.isdigit, parts[0])) and "".join(filter(str.isdigit, parts[1])):
            return {"ahead": int(parts[0]), "behind": int(parts[1])}
    except SubprocessError:
        pass
    return {"ahead": 0, "behind": 0}


def status_dirty(cwd: str) -> tuple[bool, int, int]:
    try:
        out = run(["git", "status", "--porcelain"], cwd=cwd)
    except SubprocessError:
        return False, 0, 0
    lines = [line for line in out.splitlines() if line.strip()]
    dirty = bool(lines)
    staged = sum(1 for line in lines if line[0] not in {" ", "?"})
    unstaged = sum(1 for line in lines if line[1] not in {" ", "?"})
    return dirty, staged, unstaged
