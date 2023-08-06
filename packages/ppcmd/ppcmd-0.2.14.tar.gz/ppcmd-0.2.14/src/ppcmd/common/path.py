import os


def dir_name(p) -> str:
    if not os.path.isdir(p):
        raise RuntimeError(f"p is not dir: {p}")

    return p.split("/")[-1]
