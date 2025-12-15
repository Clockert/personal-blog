"""
Integration tests for database operations
Tests CRUD operations on posts and comments
"""
import pytest
import sqlite3
import os
import sys

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import (
    get_db_connection, 
    get_all_posts, 
    get_post_by_id, 
    create_post, 
    update_post, 
    delete_post,
    get_comments_for_post,
    create_comment,
    get_all_tags,
    get_posts_by_tag
)

# Use a test database
TEST_DATABASE = 'test_blog.db'

@pytest.fixture
def test_db():
    """Set up a test database before each test"""
    # Change to test database
    import database
    database.DATABASE = TEST_DATABASE
    
    # Create tables
    conn = sqlite3.connect(TEST_DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            content TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            image_url TEXT,
            tags TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            comment_text TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    
    yield
    
    # Clean up - delete test database after test
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)

def test_create_and_get_post(test_db):
    """Test creating a post and retrieving it"""
    # Create a post
    create_post('Test Post', '2024-12-15', 'Test content', 'Test excerpt', None, 'test, python')
    
    # Get all posts
    posts = get_all_posts()
    assert len(posts) == 1
    assert posts[0]['title'] == 'Test Post'
    assert posts[0]['tags'] == 'test, python'

def test_get_post_by_id(test_db):
    """Test retrieving a specific post by ID"""
    # Create a post
    create_post('Another Post', '2024-12-15', 'Content here', 'Excerpt here', None, 'flask')
    
    # Get the post by ID
    post = get_post_by_id(1)
    assert post is not None
    assert post['title'] == 'Another Post'
    assert post['tags'] == 'flask'

def test_update_post(test_db):
    """Test updating a post"""
    # Create a post
    create_post('Original Title', '2024-12-15', 'Original content', 'Original excerpt', None, 'original')
    
    # Update the post
    update_post(1, 'Updated Title', '2024-12-15', 'Updated content', 'Updated excerpt', None, 'updated')
    
    # Verify update
    post = get_post_by_id(1)
    assert post['title'] == 'Updated Title'
    assert post['content'] == 'Updated content'
    assert post['tags'] == 'updated'

def test_delete_post(test_db):
    """Test deleting a post"""
    # Create a post
    create_post('Delete Me', '2024-12-15', 'Content', 'Excerpt', None, 'delete')
    
    # Verify it exists
    posts = get_all_posts()
    assert len(posts) == 1
    
    # Delete the post
    delete_post(1)
    
    # Verify it's gone
    posts = get_all_posts()
    assert len(posts) == 0

def test_create_and_get_comments(test_db):
    """Test creating comments for a post"""
    # Create a post first
    create_post('Post with Comments', '2024-12-15', 'Content', 'Excerpt', None, 'comments')
    
    # Create comments
    create_comment(1, 'Alice', 'Great post!', '2024-12-15 10:00')
    create_comment(1, 'Bob', 'Thanks for sharing', '2024-12-15 11:00')
    
    # Get comments
    comments = get_comments_for_post(1)
    assert len(comments) == 2
    assert comments[0]['author'] == 'Bob'  # Newest first
    assert comments[1]['author'] == 'Alice'

def test_get_all_tags(test_db):
    """Test getting all unique tags"""
    # Create posts with different tags
    create_post('Post 1', '2024-12-15', 'Content', 'Excerpt', None, 'python, flask')
    create_post('Post 2', '2024-12-15', 'Content', 'Excerpt', None, 'python, testing')
    create_post('Post 3', '2024-12-15', 'Content', 'Excerpt', None, 'flask')
    
    # Get all tags
    tags = get_all_tags()
    assert len(tags) == 3
    assert 'python' in tags
    assert 'flask' in tags
    assert 'testing' in tags

def test_get_posts_by_tag(test_db):
    """Test filtering posts by tag"""
    # Create posts with different tags
    create_post('Python Post', '2024-12-15', 'Content', 'Excerpt', None, 'python, backend')
    create_post('Flask Post', '2024-12-15', 'Content', 'Excerpt', None, 'flask, python')
    create_post('Testing Post', '2024-12-15', 'Content', 'Excerpt', None, 'testing')
    
    # Filter by 'python' tag
    python_posts = get_posts_by_tag('python')
    assert len(python_posts) == 2
    
    # Filter by 'testing' tag
    testing_posts = get_posts_by_tag('testing')
    assert len(testing_posts) == 1