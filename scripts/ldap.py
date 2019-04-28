from scripts.hydra import Exploit
class LDAP(Exploit):
    name = "ldap"
    port = 389
    def attack(self, ip_address, usernames, passwords):
        print("Running LDAP attack against IP address {ip_address} with usernames {usernames} and passwords {passwords}")
    def getloot(self, ip_address, credentials):
        pass
