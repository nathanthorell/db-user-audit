#!/usr/bin/env python
import os
import json
import csv
from sshtunnel import SSHTunnelForwarder
import utils


def main():
    "The main function"
    audit_results = []

    with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
        credentials = json.load(f)
        user = credentials["lastpass_user"]
        pwd = credentials["lastpass_pass"]
        ssh_host = credentials["ssh_host"]
        ssh_port = credentials["ssh_port"]
        ssh_user = credentials["ssh_user"]
        ssh_cert = credentials["ssh_cert"]

    serverlist = utils.get_serverlist(user, pwd)

    for server in serverlist:
        server_name = server.name.decode("utf-8")

        print("Querying", server_name, ".....")
        split_url = server.url.decode("utf-8").split("://")
        db_type = split_url[0]
        db_host = split_url[1]
        # TODO: fix this later to parse the ports properly
        if db_type == "postgres":
            db_port = 5432
        elif db_type == "mysql":
            db_port = 3306
        else:
            print("DB type unknown")
            db_port = 0

        db_login = server.username.decode("utf-8")
        db_pass = server.password.decode("utf-8")

        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=ssh_cert,
            remote_bind_address=(db_host, db_port),
            local_bind_address=("localhost", 54321),
        ) as ssh_server:
            ssh_server.start()
            local_port = ssh_server.local_bind_port

            if db_type == "postgres":
                pgconnstr = "dbname=" + db_type + " user=" + db_login + " password="
                pgconnstr += db_pass + " host=localhost" + " port=" + str(local_port)

                results_list = utils.get_pg_users(server_name, pgconnstr)
                if results_list is not None:
                    for res in results_list:
                        audit_results.append(res)
            else:
                results_list = utils.get_mysql_users(
                    server_name, db_login, db_pass, local_port
                )
                if results_list is not None:
                    for res in results_list:
                        audit_results.append(res)

    # convert json to csv output file
    with open("output.csv", "w") as outfile:
        # write a header first
        outfile.write("servername, user_login, expiration_status, user_status\n")
        # then loop through the rows
        csv_writer = csv.writer(outfile)
        for row in audit_results:
            csv_writer.writerow(row.values())


if __name__ == "__main__":
    main()
