import psycopg2
import os

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(f"dbname={os.getenv('PG_DATABASE', 'waifubot')} user={os.getenv('PG_USER', 'postgres')} password={os.getenv('PG_PASS', '')} host={os.getenv('PG_HOST', 'localhost')} port={os.getenv('PG_PORT', 5432)}")
        self.conn.autocommit = True

    def cur(self):
        return self.conn.cursor()
