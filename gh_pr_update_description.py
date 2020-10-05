#!/usr/bin/env python3

import os
import re
import sys
from dataclasses import dataclass

try:
    import click
    import git
    import github
except ImportError:
    print("pip install click gitpython pygithub", file=sys.stderr)


@dataclass
class GitInfo:
    title: str
    message: str
    apitoken: str
    branch: str
    org: str
    repo: str


def get_commit_info():
    repo = git.Repo("./")

    # get commit title + message
    commit = repo.commit("HEAD")
    title = commit.summary

    message = github.GithubObject.NotSet
    commitlines = commit.message.splitlines()
    if len(commitlines) > 1:
        message = commitlines[1:]
        # strip leading and trailing blank lines
        message = "\n".join(commitlines[1:]).strip("\n").rstrip("\n")

    # get github api token
    with repo.config_reader() as reader:
        apitoken = reader.get_value("github", "apitoken", default="")

    assert (
        apitoken
    ), "Error: set a github apitoken like `git config github.apitoken <your token>`"

    # get org + repo name from remote url
    url = list(repo.remote().urls)[0]
    m = re.match(r".*[:/](.*)/(.*)\.git$", url)  # yolo...
    org, reponame = m.groups()

    return GitInfo(
        title=title,
        message=message,
        apitoken=apitoken,
        branch=repo.active_branch,
        org=org,
        repo=reponame,
    )


def get_pr_for_branch(gitinfo):
    g = github.Github(gitinfo.apitoken)
    repo = g.get_repo("{}/{}".format(gitinfo.org, gitinfo.repo))
    pulls = repo.get_pulls()

    pr = None
    for pull in pulls:
        if pull.head.ref == str(gitinfo.branch):
            pr = pull

    assert pr, "Can't find matching pr for {}".format(gitinfo.branch)

    return pr


def update_description(pr, title, message):
    pr.edit(title=title, body=message)


@click.version_option()
@click.command()
@click.option("--yes", help="Skip prompt, just apply the change", is_flag=True)
def main(yes=False):
    """Update GitHub PR description from current repo branch"""
    # get git info
    gitinfo = get_commit_info()

    # try to find pr for this branch
    pr = get_pr_for_branch(gitinfo)

    # update description on pr
    try:
        if yes or click.confirm(
            "About to update description on {}, ready?".format(
                click.style(pr.html_url, fg="blue", bold=True)
            ),
            default="Y",
            show_default=True,
        ):
            update_description(pr, gitinfo.title, gitinfo.message)
    except click.exceptions.Abort:
        exit(-1)

    click.echo((click.style("PR successfully updated 🎉 !", fg="green")))


if __name__ == "__main__":
    main()
