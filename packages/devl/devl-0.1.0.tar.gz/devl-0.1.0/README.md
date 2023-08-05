# devl

This is a work in progress.

## Build/Deploy steps

  1. Bump version in pyproject.toml
  2. `env/bin/python -m build`
  3. `env/bin/twine upload dist/*`
