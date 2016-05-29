import psycopg2


def connect_to_db(dbname, user, password, host, port):
    conn = psycopg2.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()
    return cur, conn


def disconnect_from_db(cur, conn):
    cur.close()
    conn.close()


dbname_local = "onecityday_spb"
user_local = "postgres"
password_local = ""
host_local = "localhost"
port_local = "5432"
