import tarfile
import os.path

from dxd.ddc.common.exit_code import run

from ppcmd.common.date_format import cur_time_str
from ppcmd.common.print import print_major_cmd_step__


class PpcProcessor:
    def tgz(self, dir):
        print_major_cmd_step__(f'tgz {dir}...')
        output_filename = f'{os.path.basename(dir)}__{cur_time_str()}.tgz'
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(dir, arcname=os.path.basename(dir))
        run(f"ls -la {output_filename}")

    def update(self):
        print_major_cmd_step__('update...')

    def test(self):
        print_major_cmd_step__('test...')

    def coverage(self):
        print_major_cmd_step__('coverage...')

    def lint(self):
        print_major_cmd_step__('lint...')
