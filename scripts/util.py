import pickle, gzip, csv
from tabulate import tabulate

loot_file = "data/loot.csv"

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

def log_loot(loot, output):
    """Append list of (username, password) tuples to CSV file. Print message to output stream."""
    print(f"{Color.GRN}Logging gathered loot.{Color.END}\n" +
          "Note that sometimes only usernames are gathered, and sometimes only passwords.",
          file=output)
    old_loot = set(get_logged_loot())
    loot = list(set(loot) - old_loot)
    if not loot:
        return
    print(tabulate(loot, headers=["Usernames", "Passwords"]), file=output)
    with open(loot_file, "a") as log:
        writer = csv.writer(log)
        for item in loot:
            writer.writerow(item)

def get_logged_loot():
    """Get list of (username, password) tuples from CSV file."""
    logged_loot = []
    try:
        with open(loot_file, "r") as log:
            reader = csv.reader(log)
            for row in reader:
                # change '' to None
                for i in range(len(row)):
                    if not row[i]:
                        row[i] = None
                logged_loot.append(row)
    except FileNotFoundError:
            pass
    return tuple(tuple(l) for l in logged_loot)

def print_all_loot(output):
    """Print all of the loot logged by the program."""
    loot = get_logged_loot()
    if not loot:
        print(f"{Color.RED}No loot obtained.{Color.END}", file=output)
        return
    print(f"{Color.BGRN}Printing all gathered loot:{Color.END}")
    print(Color.BBLUE + tabulate(loot, headers=["Usernames", "Passwords"]) + Color.END, file=output)

class Color:
    # general codes
    END    = '\033[0m'
    BOLD   = '\033[1m'
    ULINE  = '\033[4m'
    # colors
    BLCK   = '\033[30m'
    RED    = '\033[31m'
    GRN    = '\033[32m'
    YLLW   = '\033[33m'
    BLUE   = '\033[34m'
    MAGEN  = '\033[35m'
    CYAN   = '\033[36m'
    WHITE  = '\033[37m'
    # bright colors
    BBLCK  = '\033[90m'
    BRED   = '\033[91m'
    BGRN   = '\033[92m'
    BYLLW  = '\033[93m'
    BBLUE  = '\033[94m'
    BMAGEN = '\033[95m'
    BCYAN  = '\033[96m'
    BWHITE = '\033[97m'
