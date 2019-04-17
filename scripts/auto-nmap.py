import nmap
import pickle

# Relevant ports:
# 22   - SSH
# 443  - HTTPS
# 80   - HTTP
# 5432 - Postgresql
# 389  - LDAP
# 636  - LDAPS

# object detailing what ports are open (and we can attack) and the host ip
class Endpoint:


    def __init__(self, host):
        pass

# function that creates endpoints of all host ip's scanned
def autonmap(host_ips):
    nm = nmap.PortScanner()
    nm.scan(hosts = host_ips, arguments= '-Pn -T4 --open -n -p 22,80,443,5432,389,636')

    port_dict = {}

    # run through all the hosts scanned and make endpoint objects based off of
    # information gathered
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            open_ports = []
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    open_ports.append(port)
        port_dict[host] = open_ports    


autonmap('45.33.32.156')