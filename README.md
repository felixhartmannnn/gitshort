

## Development

Run tests before pushing changes:

```bash
python -m pip install -e .
python -m pytest tests -q
```

Report failures as GitHub issues with pytest output and the command set used.

## Contributing

Fork the repository, create a changes branch, add a regression test for failures, and open a PR from your branch. Keep commits scoped to one concern and update README/docs when CLI behavior changes.
