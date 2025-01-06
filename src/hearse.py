import mysql.connector
from datetime import datetime
import os

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT"),
}

FETCH_QUERY = """
SELECT domain 
FROM domains 
WHERE status IN ('NXDOMAIN', 'SERVFAIL')
LIMIT %s OFFSET %s
"""

AUTHOR = "xRuffKez"
SOURCE_REPO = "https://github.com/xRuffKez/DomainGraveyard"
MAX_DOMAINS_PER_FILE = 1000000


def export_domains():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        offset = 0
        file_count = 1

        while True:
            cursor.execute(FETCH_QUERY, (MAX_DOMAINS_PER_FILE, offset))
            domains = cursor.fetchall()

            if not domains:
                break

            file_name = f"{EXPORT_DIR}/dead_{file_count}.txt"
            created_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            metadata = f"""# Source Repo: {SOURCE_REPO}
# Author: {AUTHOR}
# Number of Domains: {len(domains)}
# List Name: dead_{file_count}
# Created At: {created_time}
# This list contains domains with DNS statuses NXDOMAIN and SERVFAIL.
# You can use this list to clean your own blocklists of dead domains.
"""
          
            with open(file_name, "w") as file:
                file.write(metadata + "\n")
                for domain in domains:
                    file.write(domain[0] + "\n")

            print(f"Exported {len(domains)} domains to {file_name}")

            offset += MAX_DOMAINS_PER_FILE
            file_count += 1

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    export_domains()
