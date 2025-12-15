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

def create_post(title, date, content, excerpt, image_url, tags):
    """Insert a new post into the database"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO posts (title, date, content, excerpt, image_url, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, date, content, excerpt, image_url, tags))
    conn.commit()
    conn.close()

def update_post(post_id, title, date, content, excerpt, image_url, tags):
    """Update an existing post in the database"""
    conn = get_db_connection()
    conn.execute('''
        UPDATE posts 
        SET title = ?, date = ?, content = ?, excerpt = ?, image_url = ?, tags = ?
        WHERE id = ?
    ''', (title, date, content, excerpt, image_url, tags, post_id))
    conn.commit()
    conn.close()

def delete_post(post_id):
    """Delete a post from the database"""
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

def get_posts_by_tag(tag):
    """Get all posts that contain a specific tag"""
    conn = get_db_connection()
    # Use LIKE to search for the tag in the tags column
    # Add wildcards to match tag anywhere in the string
    posts = conn.execute(
        "SELECT * FROM posts WHERE tags LIKE ? ORDER BY date DESC",
        (f'%{tag}%',)
    ).fetchall()
    conn.close()
    return posts

def get_all_tags():
    """Get all unique tags from all posts"""
    conn = get_db_connection()
    posts = conn.execute('SELECT tags FROM posts WHERE tags IS NOT NULL AND tags != ""').fetchall()
    conn.close()
    
    # Collect all unique tags
    all_tags = set()
    for post in posts:
        if post['tags']:
            # Split tags and add to set (removes duplicates)
            tags = [tag.strip() for tag in post['tags'].split(',')]
            all_tags.update(tags)
    
    # Return as sorted list
    return sorted(all_tags)

# Only run this if we're running this file directly
if __name__ == '__main__':
    init_db()