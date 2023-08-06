import os.path

from ppcmd.common.date_format import cur_time_str
from ppcmd.common.exit_code import ExitCode, exit_with_error_msg
from ppcmd.common.print import print_major_cmd_step__
from ppcmd.common.run import run__


class PpcProcessor:
    def tgz(self, dir: str, save_loc: str):
        if not os.path.exists(save_loc):
            exit_with_error_msg(ExitCode.FAILED_TO_TGZ__SAVE_LOC_DOES_NOT_EXIST)
        if not os.path.isdir(save_loc):
            exit_with_error_msg(ExitCode.FAILED_TO_TGZ__SAVE_LOC_IS_NOT_DIR)

        print_major_cmd_step__(f'tgz {dir}...')
        dir_name = os.path.basename(dir)
        output_filename = f'{dir_name}__{cur_time_str()}.tgz'
        run__(f"tar cvzf {output_filename} {dir}")
        # with tarfile.open(output_filename, "w:gz") as tar:
        #     tar.add(dir, arcname=os.path.basename(dir))
        if save_loc == ".":
            run__(f"ls -lah {output_filename}")
        else:
            run__(f"mv {output_filename} {save_loc}")
            run__(f"ls -lah {save_loc}/{output_filename}")

    def update(self):
        print_major_cmd_step__('update...')

    def test(self):
        print_major_cmd_step__('test...')

    def coverage(self):
        print_major_cmd_step__('coverage...')

    def lint(self):
        print_major_cmd_step__('lint...')
