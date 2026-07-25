from __future__ import annotations

import os
from typing import Optional

from gitshort.polling import (
    repo_root,
    current_branch,
    upstream_branch,
    ahead_behind,
    status_dirty,
)


class RepoInfo:
    def __init__(
        self,
        root: str,
        branch: Optional[str],
        upstream: Optional[str],
        ahead: int,
        behind: int,
        dirty: bool,
        staged: int,
        unstaged: int,
    ) -> None:
        self.root = root
        self.branch = branch
        self.upstream = upstream
        self.ahead = ahead
        self.behind = behind
        self.dirty = dirty
        self.staged = staged
        self.unstaged = unstaged


def discover_repo(cwd: str = ".") -> Optional[RepoInfo]:
    root = repo_root(cwd)
    if not root:
        return None
    branch = current_branch(cwd)
    upstream = None
    ahead = 0
    behind = 0
    if branch:
        upstream = upstream_branch(branch, cwd)
        if upstream:
            ahead_behind_values = ahead_behind(cwd, branch)
            ahead = ahead_behind_values["ahead"]
            behind = ahead_behind_values["behind"]
    dirty, staged, unstaged = status_dirty(cwd)
    return RepoInfo(
        root=root,
        branch=branch,
        upstream=upstream,
        ahead=ahead,
        behind=behind,
        dirty=dirty,
        staged=staged,
        unstaged=unstaged,
    )
