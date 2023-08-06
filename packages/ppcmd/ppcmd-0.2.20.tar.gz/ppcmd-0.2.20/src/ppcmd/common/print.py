from colorama import Fore


def echo__(msg):
    print(msg)
    return msg + "\n"


def echo_info__(msg):
    print(Fore.GREEN + f"INFO: {msg}")


def echo_error__(msg):
    err_msg = f"ERROR: {msg}"
    print(Fore.RED + err_msg)
    return err_msg


def print_step__(step, color):
    print(color + f'>> {step}')


def print_major_cmd_step__(cmd):
    print_step__(cmd, Fore.YELLOW)


def print_cmd_step__(cmd):
    print_step__(cmd, Fore.BLUE)


def print_additional_explanation__(msg):
    print(Fore.CYAN + f"  : {msg}")
