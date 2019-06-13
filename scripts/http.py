import subprocess
from hydra import Exploit
from util import Color
class HTTP(Exploit):
    def __init__(self):
        self.name = 'http-get'
        self.port = 80
    def getloot(self, ip_address, credentials):
        for c in credentials:
            print(f"{Color.BBLUE}Finding files and directories on IP address {ip_address} " +
                  f"with:\n username: {c[0]} and password: {c[1]}{Color.END}",
                    file=self.output)
            # run Gobuster with credentials to find hidden paths
            command = (f'gobuster -w /usr/share/dirb/wordlists/common.txt -u http://{ip_address} -U {c[0]} -P {c[1]}').split()
            result = subprocess.run(command, capture_output=True, text=True)
            if result.stdout:
                files = []
                # format output from Gobuster
                for line in result.stdout.split('\n'):
                    if not line:
                        continue
                    if line.startswith('/'):
                        file = line.split()
                        files.append(file[0])
                # write paths out to data folder, skipping duplicates
                if files:
                    with open(f'data/{ip_address}_paths.lst', 'a+') as f:
                        old_files = set(f.read().split())
                    all_files = old_files.union(set(files))
                    with open(f'data/{ip_address}_paths.lst', 'w+') as f:
                        f.write('\n'.join(all_files) + '\n')
                print(f"{Color.BBLUE}Logging found hidden directories and files{Color.END}", file=self.output)
        return None
