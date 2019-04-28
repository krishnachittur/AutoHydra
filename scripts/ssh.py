from hydra import Exploit
class SSH(Exploit):
    name = "ssh"
    port = 22
    # def attack(self, ip_address):
    #     pass
    def getloot(self, ip_address, credentials):
        pass
