import tarfile
import os.path

from ppcmd.common.date_format import cur_time_str
from ppcmd.common.print import print_major_cmd_step__
from ppcmd.common.run import run__


class PpcProcessor:
    def tgz(self, dir):
        print_major_cmd_step__(f'tgz {dir}...')
        dir_name = os.path.basename(dir)
        output_filename = f'{dir_name}__{cur_time_str()}.tgz'
        run__(f"tar cvzf {output_filename} {dir}")
        # with tarfile.open(output_filename, "w:gz") as tar:
        #     tar.add(dir, arcname=os.path.basename(dir))
        run__(f"ls -lah {output_filename}")

    def update(self):
        print_major_cmd_step__('update...')

    def test(self):
        print_major_cmd_step__('test...')

    def coverage(self):
        print_major_cmd_step__('coverage...')

    def lint(self):
        print_major_cmd_step__('lint...')
