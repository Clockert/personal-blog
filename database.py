import sqlite3
from datetime import datetime, timezone

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

def get_all_posts(sort_by='date_desc', limit=None, offset=0):
    """Get all posts from the database with various sorting options and pagination

    Args:
        sort_by: Sort order - 'date_desc', 'date_asc', 'title_asc', 'title_desc'
        limit: Maximum number of posts to return (None for all posts)
        offset: Number of posts to skip (for pagination)
    """
    conn = get_db_connection()

    # Determine ORDER BY clause based on sort_by parameter
    if sort_by == 'date_asc':
        order_clause = 'ORDER BY created_at ASC, id ASC'
    elif sort_by == 'title_asc':
        order_clause = 'ORDER BY title ASC'
    elif sort_by == 'title_desc':
        order_clause = 'ORDER BY title DESC'
    else:  # default to date_desc
        order_clause = 'ORDER BY created_at DESC, id DESC'

    # Add LIMIT and OFFSET if specified
    query = f'SELECT * FROM posts {order_clause}'
    if limit is not None:
        query += f' LIMIT {limit} OFFSET {offset}'

    posts = conn.execute(query).fetchall()
    conn.close()
    return posts

def get_posts_count():
    """Get the total count of posts in the database"""
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    conn.close()
    return count

def get_post_by_id(post_id):
    """Get a single post by its ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post

def create_post(title, content, excerpt, image_url, tags):
    """Insert a new post into the database

    Timestamps (created_at, updated_at) are automatically set by the database.
    The date field is set to current date for display purposes.
    """
    conn = get_db_connection()
    # Generate display date
    date = datetime.now().strftime('%Y-%m-%d')
    # created_at and updated_at are automatically set by database DEFAULT
    conn.execute('''
        INSERT INTO posts (title, date, content, excerpt, image_url, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, date, content, excerpt, image_url, tags))
    conn.commit()
    conn.close()

def update_post(post_id, title, date, content, excerpt, image_url, tags):
    """Update an existing post in the database

    Updates the updated_at timestamp automatically.
    """
    conn = get_db_connection()
    # Generate current timestamp for updated_at
    updated_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('''
        UPDATE posts
        SET title = ?, date = ?, content = ?, excerpt = ?, image_url = ?, tags = ?, updated_at = ?
        WHERE id = ?
    ''', (title, date, content, excerpt, image_url, tags, updated_at, post_id))
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
        "SELECT * FROM posts WHERE tags LIKE ? ORDER BY created_at DESC, id DESC",
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

def get_comments_for_post(post_id):
    """Get all comments for a specific post, ordered by date (newest first)"""
    conn = get_db_connection()
    comments = conn.execute(
        'SELECT * FROM comments WHERE post_id = ? ORDER BY date DESC',
        (post_id,)
    ).fetchall()
    conn.close()
    return comments

def create_comment(post_id, author, comment_text, date):
    """Insert a new comment into the database"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO comments (post_id, author, comment_text, date)
        VALUES (?, ?, ?, ?)
    ''', (post_id, author, comment_text, date))
    conn.commit()
    conn.close()

def delete_comment(comment_id):
    """Delete a comment from the database"""
    conn = get_db_connection()
    conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()

# Only run this if we're running this file directly
if __name__ == '__main__':
    init_db()