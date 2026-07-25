# gitshort

Compact, local-first `git` repository status snapshot tool.

## What it does

`gitshort` summarizes a repository in one scannable block without stashing, checking out, or mutating the working tree:

- detected repo root, current branch, and upstream
- ahead/behind counts from the upstream tracking ref
- working-tree change counts in one line
- optional JSON mode for scripts and CI

## Installation

```bash
python -m pip install .
```

After installing, `gitshort` is on your PATH.

## Usage

```bash
gitshort [path]
gitshort path --json
gitshort path --no-upstream
```

Default `path` is `.`.

## Example

```
? my-project
  branch: feature/dashboard
  origin/main: ahead 3 / behind 0
  changes: dirty (2 insertions, 1 staged, 1 unstaged)
```

## Project structure

```
src/gitshort/
  cli.py
  formatting.py
  importer.py
  polling.py
tests/
  test_suite.py
pyproject.toml
README.md
```

## License

MIT
