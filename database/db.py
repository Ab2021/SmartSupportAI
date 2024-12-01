import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                print("[DEBUG] Attempting database connection...")
                self.conn = psycopg2.connect(
                    host=os.environ['PGHOST'],
                    database=os.environ['PGDATABASE'],
                    user=os.environ['PGUSER'],
                    password=os.environ['PGPASSWORD'],
                    port=os.environ['PGPORT']
                )
                print("[DEBUG] Successfully connected to database")
                return
            except psycopg2.Error as e:
                retry_count += 1
                print(f"[DEBUG] Database connection attempt {retry_count} failed: {str(e)}")
                if retry_count < self.max_retries:
                    time.sleep(2)  # Wait before retrying
                else:
                    raise Exception("Failed to connect to database after maximum retries")

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
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO tickets (title, description, category, priority)
                       VALUES (%s, %s, %s, %s) RETURNING id""",
                    (title, description, category, priority)
                )
                ticket_id = cur.fetchone()[0]
                self.conn.commit()
                print(f"[DEBUG] Successfully saved ticket with ID: {ticket_id}")
                return ticket_id
        except psycopg2.Error as e:
            print(f"[DEBUG] Error saving ticket to database: {str(e)}")
            self.conn.rollback()
            raise

    def get_knowledge_base_entries(self, category=None):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                if category:
                    cur.execute("SELECT * FROM knowledge_base WHERE category = %s", (category,))
                else:
                    cur.execute("SELECT * FROM knowledge_base")
                entries = cur.fetchall()
                print(f"[DEBUG] Retrieved {len(entries)} knowledge base entries")
                return entries
        except psycopg2.Error as e:
            print(f"[DEBUG] Error fetching knowledge base entries: {str(e)}")
            raise

db = Database()
