# colors.py
# Text formatting using Minecraft color codes.
# https://github.com/woidzero/MCFC.git


BLACK = '\033[30m'
DARK_BLUE = '\033[34m'
DARK_GREEN = '\033[32m'
DARK_AQUA = '\033[36m'
DARK_RED = '\033[31m'
DARK_PURPLE = '\033[35m'
GOLD = '\033[33m'
GRAY = '\033[0;37;40m'
DARK_GRAY = '\033[1;30;40m'
BLUE = '\033[1;34;40m'
GREEN = '\033[1;32;40m'
AQUA = '\u001b[36;1m'
RED = '\u001b[31;1m'
LIGHT_PURPLE = '\u001b[35;1m'
YELLOW = '\033[1;33;40m'
WHITE = '\u001b[37m'
RESET = '\u001b[0m'


colorCodes = {
    "&0": BLACK,
    "&1": DARK_BLUE,
    "&2": DARK_GREEN,
    "&3": DARK_AQUA,
    "&4": DARK_RED,
    "&5": DARK_PURPLE,
    "&6": GOLD,
    "&7": GRAY,
    "&8": DARK_GRAY,
    "&9": BLUE,
    "&a": GREEN,
    "&b": AQUA,
    "&c": RED,
    "&d": LIGHT_PURPLE,
    "&e": YELLOW,
    "&f": WHITE,
    "&r": RESET,
}