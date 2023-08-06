from colorama import init
import fire

from ppcmd.ppc.ppc_processor import PpcProcessor

processor = PpcProcessor()


class PPC(object):
    def tgz(self, dir, out_dir ="."):
        """Tgz dir."""
        processor.tgz(dir, save_loc=out_dir)

    def update(self):
        """Update ppc command."""
        processor.update()

    def test(self):
        """Run unit test."""
        processor.test()

    def cov(self):
        """Run coverage report."""
        processor.coverage()

    def lint(self):
        """Run lint report."""
        processor.lint()


def main_():
    init_ppc_pkg()
    fire.Fire(PPC)


def init_ppc_pkg():
    init(autoreset=True) # color auto reset
