"""
The environment a test's own throwaway repository runs git in.

Git exports `GIT_*` variables to every hook it runs, so that the hook's own git
commands find the repository. The pre-commit hook runs this suite, and every
child process the suite starts inherits them.
- **From the main checkout** git exports no `GIT_DIR`, and `GIT_INDEX_FILE` is
  the relative `.git/index`. A child that runs git in another directory
  resolves that inside its own repository, and nothing leaks.
- **From a linked worktree** both are absolute paths into this repository's
  `.git`. A test that hands that environment to a throwaway repository's git
  writes into the real one instead:
  - its `git init` re-initializes it as bare, `core.bare = true` in the shared
    `.git/config`;
  - its `git config` sets the fixture's identity there;
  - its commits land on the worktree's branch.

That broke `git status` in the main checkout on 2026-11-02, when it stopped a
paid run's resume, and again on 2026-11-10.

So every test that runs git over a repository of its own runs it in
`isolated_git_env()`: this process's environment with no `GIT_*` variable at
all, plus whatever the test sets.
"""

from __future__ import annotations

import os


def isolated_git_env(**extra: str) -> dict[str, str]:
    """This process's environment without its `GIT_*` variables, with `extra`."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(extra)
    return env
