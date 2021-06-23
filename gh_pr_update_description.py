#!/usr/bin/env python3

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
    repos: list


def get_commit_info(commitish):
    repo = git.Repo("./")

    # get commit title + message
    commit = repo.commit(commitish)
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

    # get org + repo names from remote urls
    repos = []
    for remote in repo.remotes:
        url = remote.url
        m = re.match(r".*github\.com[:/](.*?)\/(.*?)(\.git)?$", url)  # yolo...
        assert m, "Error couldn't parse org+reponame from {}".format(url)
        org, reponame, _ = m.groups()
        repos.append("{}/{}".format(org, reponame))

    return GitInfo(
        title=title,
        message=message,
        apitoken=apitoken,
        branch=repo.active_branch,
        repos=repos,
    )


def get_pr_for_branch(gitinfo):
    g = github.Github(gitinfo.apitoken)
    pulls = []
    for reponame in gitinfo.repos:
        repo = g.get_repo(reponame)
        pulls.append(repo.get_pulls())

    pr = None
    for pull_list in pulls:
        for pull in pull_list:
            if pull.head.ref == str(gitinfo.branch):
                pr = pull

    assert pr, "Can't find matching pr for {}".format(gitinfo.branch)

    return pr


def update_description(pr, title, message):
    pr.edit(title=title, body=message)


@click.version_option()
@click.command()
@click.option("--yes", help="Skip prompt, just apply the change", is_flag=True)
@click.option(
    "--commitish",
    help="Specify commit-ish to use for description message",
    default="HEAD",
    show_default=True,
)
def main(yes, commitish):
    """Update GitHub PR description from current repo branch"""
    # get git info
    gitinfo = get_commit_info(commitish)

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
            click.echo((click.style("PR successfully updated 🎉 !", fg="green")))
    except click.exceptions.Abort:
        pass


if __name__ == "__main__":
    main()
