import pickle, gzip

def read_gz(filename):
    """Read pickle object from gzip file"""
    try:
        with gzip.open(filename, 'rb') as handle:
            return pickle.load(handle)
    except FileNotFoundError as e:
        return None

def write_gz(filename, item):
    """Write pickle object to gzip file"""
    with gzip.open(filename, 'wb') as handle:
        pickle.dump(item, handle, protocol=pickle.HIGHEST_PROTOCOL)

class Color:
    """Useful ANSI escape sequences for different colors in terminal.
    copied from https://stackoverflow.com/a/287944
    and https://unix.stackexchange.com/a/93872"""
    # general codes
    END    = '\033[0m'
    BOLD   = '\033[1m'
    ULINE  = '\033[4m'
    # ANSI foreground colors
    BLCK   = '\033[30m'
    RED    = '\033[31m'
    GRN    = '\033[32m'
    YLLW   = '\033[33m'
    BLUE   = '\033[34m'
    MAGEN  = '\033[35m'
    CYAN   = '\033[36m'
    WHITE  = '\033[37m'
    # bright aixterm colors
    BBLCK  = '\033[90m'
    BRED   = '\033[91m'
    BGRN   = '\033[92m'
    BYLLW  = '\033[93m'
    BBLUE  = '\033[94m'
    BMAGEN = '\033[95m'
    BCYAN  = '\033[96m'
    BWHITE = '\033[97m'
