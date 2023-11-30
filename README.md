# DB User Audit

This is a database user auditing tool to generate a consolidated report of users across multiple databases.

## Local Env Setup

1. python -m venv .venv/
1. source .venv/bin/activate
1. python -m pip install -r ./requirements.txt

## Run Process

1. Update config.json with appropriate values
1. python main.py

## Notes

- Currently supports only mySQL and PostgreSQL databases
- Currently only outputs to csv
- Currently assumes server listing is in LastPass
