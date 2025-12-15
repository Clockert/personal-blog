import sqlite3

# Database file path
DATABASE = 'blog.db'

def get_db_connection():
    """Create a connection to the database"""
    conn = sqlite3.connect(DATABASE)
    # This makes rows behave like dictionaries - you can access columns by name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database using schema.sql"""
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized!")

def get_all_posts():
    """Get all posts from the database, ordered by date (newest first)"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY date DESC').fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    """Get a single post by its ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post

# Only run this if we're running this file directly
if __name__ == '__main__':
    init_db()