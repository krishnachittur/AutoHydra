# AutoHydra
AutoHydra automates nmap scans and hydra attacks against exposed ports requiring authentication on a specified IP range. Any cracked usernames and passwords are cached and reused against other endpoints automatically. Usage of wordlists such as `rockyou.txt` are encouraged.

## Dependencies

### Python Dependencies

1. nmap - http://xael.org/norman/python/python-nmap/python-nmap-0.4.1.tar.gz
Note: the version available to pip may not be a compatible version
2. psycopg2
3. paramiko

### Non-Python Dependencies

1. nmap
2. hydra
3. ldapsearch

## Supported Attack Vectors

AutoHydra can perform automated scans and attacks against the following authenticated endpoints:

1. SSH (port 22)
2. HTTP-Auth (port 80)
3. Postgres (port 5432)
4. LDAP (port 389)

Run `python3 scripts/main.py --help` for information on command-line parameters.