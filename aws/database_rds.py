import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ["RDS_HOST"],
        port=3306,
        database="league_stats",
        user=os.environ["RDS_USER"],
        password=os.environ["RDS_PASS"]
    )
