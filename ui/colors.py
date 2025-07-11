try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS = {
        "red": Fore.LIGHTRED_EX + Style.BRIGHT,
        "green": Fore.LIGHTGREEN_EX + Style.BRIGHT,
        "cyan": Fore.LIGHTCYAN_EX + Style.BRIGHT,
        "yellow": Fore.LIGHTYELLOW_EX + Style.BRIGHT,
        "blue": Fore.LIGHTBLUE_EX + Style.BRIGHT,
        "magenta": Fore.LIGHTMAGENTA_EX + Style.BRIGHT,
        "reset": Style.RESET_ALL,
        "white": Fore.WHITE + Style.BRIGHT,
    }
    def c(color, text): return COLORS.get(color, "") + str(text) + COLORS["reset"]
except ImportError:
    def c(color, text): return str(text)