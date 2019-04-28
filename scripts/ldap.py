from hydra import Exploit
class LDAP(Exploit):
    name = "ldap"
    port = 389
    def attack(self, ip_address, usernames, passwords):
        print(f"Running LDAP attack against IP address {ip_address} with usernames {usernames} and passwords {passwords} on domain {self.domain}")
        common_usernames = ['root', 'admin', 'user']
        common_groups = ['admins', 'users']
    def getloot(self, ip_address, credentials):
        pass
