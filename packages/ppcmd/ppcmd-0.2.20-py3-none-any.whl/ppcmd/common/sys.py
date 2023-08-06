import multiprocessing


def cpu_core_count():
    return multiprocessing.cpu_count()
