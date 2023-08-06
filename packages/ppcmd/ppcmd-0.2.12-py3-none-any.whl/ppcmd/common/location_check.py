import os


def is_git_root__():
    return os.path.exists('.git')
