"""Choose M for the Distiller's shadow step in `.github/workflows/distiller.yml`.

M is the newest commit that is the merge-base of the PR, or one of its
ancestors, and has an artifact `coverage-at-m-<sha>`:

    git merge-base origin/<base branch> HEAD     the base branch first
    git rev-list <merge-base>                    walked from its first line

stopping at the first commit that has one. In CI, HEAD is the PR's merge
commit, whose first parent is the tip of the base branch, so the merge-base is
that tip and not the commit the PR branched from.

An artifact counts only if it has not expired, its name carries a full sha, and
the run that uploaded it is a run of this repository, on the base branch, at
that same commit. A PR's run executes its own copy of the workflow and can
upload an artifact under any name, but a fork's run belongs to another
repository and a PR's run to the PR's head branch. Of several artifacts with
one name, the newest is taken.

The input is the artifact list as JSON lines, one object of
`GET /repos/{owner}/{repo}/actions/artifacts` per line, which is what the
workflow writes with `gh api --paginate --jq`. It prints `<M> <run id>`, or
nothing when no commit qualifies, and says on stderr what it looked at. It exits
non-zero only when it could not look — git failed, or a line is not an
artifact — which is not the same as finding nothing.

Standard library only, and the workflow runs it with `python -I`.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys

PREFIX = "coverage-at-m-"
FULL_SHA = re.compile(r"[0-9a-f]{40}")


def log(message: str) -> None:
    print(f"choose_m: {message}", file=sys.stderr)


def git(*args: str) -> str:
    try:
        return subprocess.run(("git", *args), check=True, capture_output=True,
                              text=True).stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"choose_m: git {' '.join(args)} failed: "
                         f"{e.stderr.strip()}") from None


def rejection(artifact: dict, sha: str, base_branch: str) -> str | None:
    """Why this `coverage-at-m-<sha>` artifact does not count, or None."""
    if artifact.get("expired") is not False:
        return "expired"
    run = artifact.get("workflow_run")
    if not isinstance(run, dict) or not isinstance(run.get("id"), int):
        return "without a run"
    if (run.get("repository_id") is None
            or run.get("head_repository_id") != run.get("repository_id")):
        return "from another repository"
    if run.get("head_branch") != base_branch:
        return "from another branch"
    if run.get("head_sha") != sha:
        return "from another commit"
    return None


def newer(a: dict, b: dict) -> bool:
    return ((a.get("created_at") or "", a.get("id") or 0)
            > (b.get("created_at") or "", b.get("id") or 0))


def qualifying(lines, base_branch: str):
    """`({sha: artifact}, Counter)`: the newest artifact that counts for each
    commit, and why each of the others named `coverage-at-m-*` did not."""
    best: dict[str, dict] = {}
    rejected: collections.Counter = collections.Counter()
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            artifact = json.loads(line)
        except json.JSONDecodeError as e:
            raise SystemExit(f"choose_m: line {number} of the artifact list "
                             f"is not JSON: {e}") from None
        if not isinstance(artifact, dict) or not isinstance(artifact.get("name"), str):
            raise SystemExit(f"choose_m: line {number} of the artifact list "
                             "is not an artifact")
        name = artifact["name"]
        if not name.startswith(PREFIX):
            continue
        sha = name[len(PREFIX):]
        why = ("without a full sha" if not FULL_SHA.fullmatch(sha)
               else rejection(artifact, sha, base_branch))
        if why:
            rejected[why] += 1
        elif sha not in best or newer(artifact, best[sha]):
            best[sha] = artifact
    return best, rejected


def choose(commits, best: dict):
    """The first of `commits` with an artifact that counts, as
    `(distance, sha, artifact)`, or None."""
    for distance, sha in enumerate(commits):
        if sha in best:
            return distance, sha, best[sha]
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Choose M for the Distiller's shadow step.")
    parser.add_argument("--base-branch", required=True,
                        help="the PR's base branch, as GITHUB_BASE_REF names it")
    parser.add_argument("--artifacts", required=True,
                        help="the artifact list, as JSON lines")
    args = parser.parse_args(argv)

    merge_base = git("merge-base", f"origin/{args.base_branch}", "HEAD").strip()
    commits = git("rev-list", merge_base).split()
    try:
        with open(args.artifacts, encoding="utf-8") as f:
            best, rejected = qualifying(f, args.base_branch)
    except OSError as e:
        raise SystemExit(f"choose_m: cannot read the artifact list: {e}") from None

    log(f"merge-base of origin/{args.base_branch} and HEAD: {merge_base}")
    not_counted = ", ".join(f"{n} {why}" for why, n in sorted(rejected.items()))
    log(f"commits with a coverage artifact that counts: {len(best)}"
        + (f"; not counted: {not_counted}" if not_counted else ""))

    found = choose(commits, best)
    if found is None:
        log(f"none of them is the merge-base or one of its "
            f"{len(commits) - 1} ancestors")
        return 0
    distance, sha, artifact = found
    run = artifact["workflow_run"]
    where = ("the merge-base itself" if distance == 0
             else f"{distance} commit{'s' * (distance != 1)} below the merge-base")
    log(f"M = {sha}, {where}: artifact {artifact.get('id')} of run {run['id']}, "
        f"created {artifact.get('created_at')}")
    print(sha, run["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
