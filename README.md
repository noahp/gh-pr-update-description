[![GitHub](https://img.shields.io/badge/GitHub-noahp%2Fgh--pr--update--description-8da0cb?style=for-the-badge&logo=github)](https://github.com/noahp/gh-pr-update-description)
[![PyPI
version](https://img.shields.io/pypi/v/gh-pr-update-description.svg?style=for-the-badge)](https://pypi.org/project/gh-pr-update-description/)
[![PyPI
pyversions](https://img.shields.io/pypi/pyversions/gh-pr-update-description.svg?style=for-the-badge)](https://pypi.python.org/pypi/gh-pr-update-description/)

# 🔃 GitHub PR Update Description

Python script to attempt to refresh the github PR description with the top
commit.

_Note: the [`gh` cli tool](https://github.com/cli/cli) permits pretty similar
functionality (plus a TON more), via for example:_

```bash
# use git log to get the current commit message subject + body, and pass to gh
gh pr edit \
  --title "$(git log -n1 --format='%s')" \
  --body "$(git log -n1 --format='%b')"
```

## Usage

Requires a github token available from git config, eg:

```bash
git config github.apitoken <your token>
```

```bash
❯ pip install gh-pr-update-description

❯ gh-pr-update-description
About to update description on https://github.com/foo/bar/pull/128, ready? [Y/n]:
PR successfully updated 🎉 !
```
