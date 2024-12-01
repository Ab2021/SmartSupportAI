import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ['PGHOST'],
            database=os.environ['PGDATABASE'],
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'],
            port=os.environ['PGPORT']
        )
        self._create_tables()

    def _create_tables(self):
        with self.conn.cursor() as cur:
            # Create tickets table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT,
                    priority INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create knowledge_base table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT,
                    tags TEXT[]
                )
            """)
            self.conn.commit()

    def save_ticket(self, title, description, category=None, priority=None):
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO tickets (title, description, category, priority)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (title, description, category, priority)
            )
            ticket_id = cur.fetchone()[0]
            self.conn.commit()
            return ticket_id

    def get_knowledge_base_entries(self, category=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            if category:
                cur.execute("SELECT * FROM knowledge_base WHERE category = %s", (category,))
            else:
                cur.execute("SELECT * FROM knowledge_base")
            return cur.fetchall()

db = Database()
