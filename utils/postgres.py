from datetime import datetime
import psycopg2
import psycopg2.extras


def get_pg_users(server, connstring):
    """connects to a postgres server and queries the logins
    returns hostname, user_login, expiration_status, user_type
    """
    try:
        conn = psycopg2.connect(connstring)
        cmd = f"""
            SELECT '{server}' AS servername, rolname AS user_login,
        CASE WHEN rolvaliduntil IS NOT NULL THEN rolvaliduntil::text
        ELSE 'active' END AS expiration_status,
        CASE WHEN rolsuper = true THEN 'superuser'
        ELSE 'normal' END AS user_type
        FROM pg_roles WHERE rolcanlogin = true
        AND (rolname NOT IN ('rdsadmin', 'masterdba', 'monitor_ro')
           AND rolname NOT LIKE '%_ro' AND rolname NOT LIKE '%_rw')
        ORDER BY rolsuper DESC, rolname;
        """
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(cmd)
        db_results = cur.fetchall()
        db_result_dict = []
        for row in db_results:
            db_result_dict.append(dict(row))
        return db_result_dict

    except psycopg2.Error as err:
        print(str(datetime.now()) + " - Connection issue with: " + server)
        print(err)
