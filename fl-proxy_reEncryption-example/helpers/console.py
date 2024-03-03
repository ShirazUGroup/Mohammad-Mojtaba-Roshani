from colorama import Fore, Back, Style, init


class Console:
    def __init__(self) -> None:
        init()

    def bg_red(self, text: str) -> None:
        print(Back.RED + text + Style.RESET_ALL)

    def bg_blue(self, text: str) -> None:
        print(Back.BLUE + text + Style.RESET_ALL)

    def error(self, text: str) -> None:
        print(Fore.RED + f"ERROR>\t{text}" + Style.RESET_ALL)

    def debug(self, debug: bool,  text: str) -> None:
        if debug:
            print(Fore.CYAN + f"DEBUG>\t{text}" + Style.RESET_ALL)

    def warn(self, text: str) -> None:
        print(Fore.YELLOW + text + Style.RESET_ALL)

    def success(self, text: str) -> None:
        print(Fore.GREEN + f"SUCCESS> {text}" + Style.RESET_ALL)
