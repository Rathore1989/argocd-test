from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'database-service')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'mydb')
DB_USER = os.getenv('POSTGRES_USER', 'user')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'password')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Hello World! Database version: {db_version[0]}"
    except Exception as e:
        return f"Hello World! (Database connection failed: {str(e)})"

@app.route('/initdb')
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hits (
            id SERIAL PRIMARY KEY,
            count INTEGER NOT NULL
        );
    ''')
    
    # Initialize counter if empty
    cur.execute('SELECT COUNT(*) FROM hits')
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO hits (count) VALUES (0)')
    
    conn.commit()
    cur.close()
    conn.close()
    return "Database initialized"

@app.route('/count')
def count_hits():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Increment counter
    cur.execute('UPDATE hits SET count = count + 1 WHERE id = 1 RETURNING count')
    count = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    return f"This page has been visited {count} times"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
