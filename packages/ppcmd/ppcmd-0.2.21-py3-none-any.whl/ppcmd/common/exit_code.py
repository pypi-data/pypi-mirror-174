import sys
from enum import Enum

from ppcmd.common.run import is_failed, run__
from ppcmd.common.print import echo_error__


class ExitCode(Enum):
    UNDEFINED = 9999
    SUCCEED = 0
    NOT_GIT_ROOT_DIR = 10
    FAILED_TO_TEST = 101
    FAILED_TO_COV = 201
    FAILED_TO_REPORT_COV_RESULT = 211
    FAILED_TO_LINT = 301
    FAILED_TO_PACK = 401
    FAILED_TO_DEPLOY = 501
    FAILED_TO_TGZ = 601
    FAILED_TO_TGZ__SAVE_LOC_DOES_NOT_EXIST = 602
    FAILED_TO_TGZ__SAVE_LOC_IS_NOT_DIR = 603


exit_code_msg = {
    ExitCode.UNDEFINED: "undefined exit code.",
    ExitCode.SUCCEED: "succeed.",
    ExitCode.NOT_GIT_ROOT_DIR: "not git root dir.",
    ExitCode.FAILED_TO_TEST: "failed to test",
    ExitCode.FAILED_TO_COV: "failed to cov",
    ExitCode.FAILED_TO_REPORT_COV_RESULT: "failed to report cov result.",
    ExitCode.FAILED_TO_LINT: "failed to lint.",
    ExitCode.FAILED_TO_PACK: "failed to pack.",
    ExitCode.FAILED_TO_DEPLOY: "failed to deploy.",
    ExitCode.FAILED_TO_TGZ: "failed to tgz.",
    ExitCode.FAILED_TO_TGZ__SAVE_LOC_DOES_NOT_EXIST: "save location does not exist.",
    ExitCode.FAILED_TO_TGZ__SAVE_LOC_IS_NOT_DIR: "save location is not directory.",
}


def run(cmd: str, ppc_fail_exit_code: ExitCode = ExitCode.UNDEFINED):
    exit_code = run__(cmd)
    if is_failed(exit_code):
        exit_with_error_msg(ppc_fail_exit_code)


def exit_with_error_msg(exit_code: ExitCode):
    echo_error__(exit_code_msg[exit_code])
    sys.exit(exit_code.value)
