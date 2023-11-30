import pymysql.cursors


def get_mysql_users(server, db_login, db_pass, db_port):
    "connects to mysql and queries the users"
    try:
        conn = pymysql.connect(
            database="mysql",
            user=db_login,
            password=db_pass,
            host="localhost",  # this is because of the SSH tunnel
            port=db_port,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn:
            with conn.cursor() as cur:
                cmd = f"""
                SELECT '{server}' AS servername, user, password_expired
                FROM mysql.user
                WHERE (user NOT IN ('monitoring', 'rdsadmin', 'mysql.sys')
                   AND user NOT LIKE '_ro' AND user NOT LIKE '_rw')
                ORDER BY user;
                """
                cur = conn.cursor()
                cur.execute(cmd)
                db_results = cur.fetchall()
                return db_results
    except Exception as err:
        print(err)
