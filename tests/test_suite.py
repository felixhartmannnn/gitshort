from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import pytest

from gitshort import discover_repo, render_text, render_json
from gitshort.importer import RepoInfo
from gitshort.cli import main


def _init_repo(path: Path, branch: str = "main") -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-b", branch, str(path)], check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.invalid"], cwd=path, check=True
    )
    subprocess.run(["git", "config", "user.name", "test"], cwd=path, check=True)
    return path


def _write(path: Path, name: str, content: str) -> None:
    file_path = path / name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)


def _add_commit(path: Path) -> None:
    _write(path, "file.txt", "seed")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "seed"], cwd=path, check=True)


def test_repo_info_fields_for_dirty_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = _init_repo(Path(tmp), branch="main")
        _add_commit(repo)
        _write(repo, "file.txt", "changed")
        info: Optional[RepoInfo] = discover_repo(str(repo))
        assert info is not None
        assert info.branch == "main"
        assert info.dirty is True
        assert info.unstaged == 1
        assert info.staged == 0


def test_clean_repo_is_not_dirty() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = _init_repo(Path(tmp), branch="main")
        _add_commit(repo)
        info: Optional[RepoInfo] = discover_repo(str(repo))
        assert info is not None
        assert info.dirty is False
        assert info.staged == 0
        assert info.unstaged == 0


def test_non_git_path_returns_none() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        info: Optional[RepoInfo] = discover_repo(tmp)
        assert info is None


def test_text_output_shape() -> None:
    repo = RepoInfo(
        root="/tmp/x/my-app",
        branch="fix/issue-1",
        upstream="origin/main",
        ahead=1,
        behind=1,
        dirty=True,
        staged=1,
        unstaged=1,
    )
    text = render_text(repo)
    assert "branch: fix/issue-1" in text
    assert "origin/main: ahead 1 / behind 1" in text
    assert "dirty" in text


def test_json_output_shape() -> None:
    repo = RepoInfo(
        root="/tmp/x/my-app",
        branch="feature",
        upstream="origin/main",
        ahead=1,
        behind=0,
        dirty=False,
        staged=3,
        unstaged=2,
    )
    payload = json.loads(render_json(repo))
    assert payload["root"] == "/tmp/x/my-app"
    assert payload["dirty"] is False
    assert payload["ahead"] == 1


def test_cli_non_repo_returns_nonzero() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rc = main([tmp])
        assert rc == 2


def test_cli_clean_repo_returns_zero() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = _init_repo(Path(tmp), branch="main")
        _add_commit(repo)
        rc = main([str(repo)])
        assert rc == 0


def test_cli_dirty_repo_returns_one() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = _init_repo(Path(tmp), branch="main")
        _add_commit(repo)
        _write(repo, "t.txt", "4")
        rc = main([str(repo)])
        assert rc == 1


def test_no_upstream_flag_is_accepted() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = _init_repo(Path(tmp), branch="alt")
        _add_commit(repo)
        rc = main([str(repo), "--no-upstream"])
        assert rc == 0
