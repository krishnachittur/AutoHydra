import nmap

# function that creates endpoints of all host ip's scanned
def autonmap(host_ips):
    nm = nmap.PortScanner()
    nm.scan(hosts = host_ips, arguments= '-T4 --open -Pn -n --script "http-auth" -p 22,80,5432,389')

    host_openings = {}

    services = {
        22:'ssh',
        80:'http',
        5432:'postgres',
        389:'ldap',
    }

    # run through all the hosts scanned and make endpoint objects based off of
    # information gathered
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            open_services = []
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    if (port == 80) and ('script' not in nm[host][proto][port] or "http-auth" not in nm[host][proto][port]['script']):
                        continue
                    if port in services:
                        open_services.append(services[port])
        if open_services:
            host_openings[host] = open_services
    
    return host_openings
