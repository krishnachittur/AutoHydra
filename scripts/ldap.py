from scripts.hydra import Exploit
class LDAP(Exploit):
    name = "ldap"
    port = 389
    def attack(self, ip_address):
        pass
    def getloot(self, ip_address, credentials):
        pass
