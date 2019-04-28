from scripts.hydra import Exploit
class LDAP(Exploit):
    name = "ldap"
    port = 389
    def attack(self, ip_address, usernames, passwords):
        print(f"Running LDAP attack against IP address {ip_address} with usernames {usernames} and passwords {passwords} on domain {self.domain}")
    def getloot(self, ip_address, credentials):
        pass
