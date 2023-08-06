from pygit2 import Repository, GIT_SORT_TOPOLOGICAL


def git_last_log() -> str:
    repo = Repository('.git')
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
        return commit.message
