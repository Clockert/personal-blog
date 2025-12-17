"""
End-to-end tests for Flask application
Tests user flows and routes
"""
import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import database

TEST_DATABASE = 'test_blog.db'

@pytest.fixture
def client():
    """Set up Flask test client"""
    # Use test database
    database.DATABASE = TEST_DATABASE

    # Set up test config
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'

    # Set test credentials with hashed password
    # Hash of 'password123' for testing
    os.environ['ADMIN_USERNAME'] = 'admin'
    os.environ['ADMIN_PASSWORD_HASH'] = 'pbkdf2:sha256:1000000$933xnSwzgy0cer7z$017aa78b91a809820ff2920c2d3103257e4dfec692b04cd897a4246ac457dd49'

    # Initialize test database
    database.init_db()

    # Add a test post
    database.create_post('Test Post', 'Test content for testing', 'Test excerpt', None, 'test, flask')

    with app.test_client() as client:
        yield client

    # Clean up
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)

def test_home_page(client):
    """Test that home page loads and shows posts"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to My Blog' in response.data
    assert b'Test Post' in response.data

def test_individual_post_page(client):
    """Test that individual post page loads"""
    response = client.get('/blog/1')
    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'Test content for testing' in response.data

def test_post_not_found(client):
    """Test 404 for non-existent post"""
    response = client.get('/blog/999')
    assert response.status_code == 404

def test_login_page_loads(client):
    """Test that login page loads"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_success(client):
    """Test successful login"""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_login_failure(client):
    """Test failed login with wrong credentials"""
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'wrong'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data

def test_logout(client):
    """Test logout functionality"""
    # Login first
    client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    
    # Then logout
    response = client.get('/logout', follow_redirects=True)
    assert b'logged out' in response.data

def test_create_post_requires_login(client):
    """Test that creating post requires login"""
    response = client.get('/blog/new', follow_redirects=True)
    assert b'Please log in' in response.data

def test_create_post_when_logged_in(client):
    """Test creating a new post when logged in"""
    # Login first
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'admin'
    
    # Create post
    response = client.post('/blog/new', data={
        'title': 'New Test Post',
        'content': 'This is new content',
        'excerpt': 'New excerpt',
        'tags': 'new, test'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Post created successfully' in response.data

def test_add_comment(client):
    """Test adding a comment to a post"""
    response = client.post('/blog/1', data={
        'author': 'Test User',
        'comment_text': 'This is a test comment'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Comment added successfully' in response.data
    assert b'Test User' in response.data
    assert b'This is a test comment' in response.data

def test_tag_filtering(client):
    """Test filtering posts by tag"""
    response = client.get('/tag/test')
    assert response.status_code == 200
    assert b'Posts tagged with' in response.data
    assert b'test' in response.data

def test_delete_post_requires_login(client):
    """Test that deleting post requires login"""
    response = client.post('/blog/1/delete', follow_redirects=True)
    assert b'Please log in' in response.data

def test_edit_post_requires_login(client):
    """Test that editing post requires login"""
    response = client.get('/blog/1/edit', follow_redirects=True)
    assert b'Please log in' in response.data

def test_about_page(client):
    """Test that about page loads"""
    response = client.get('/about')
    assert response.status_code == 200

def test_blog_pagination(client):
    """Test blog pagination"""
    # Create multiple posts
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'admin'

    for i in range(8):
        database.create_post(f'Post {i}', 'Content', 'Excerpt', None, 'test')

    # Test page 1
    response = client.get('/blog?page=1')
    assert response.status_code == 200

    # Test page 2
    response = client.get('/blog?page=2')
    assert response.status_code == 200

def test_blog_sorting(client):
    """Test blog sorting by date"""
    # Test default sort (date_desc)
    response = client.get('/blog')
    assert response.status_code == 200

    # Test explicit sort parameter
    response = client.get('/blog?sort=date_desc')
    assert response.status_code == 200

def test_edit_post_functionality(client):
    """Test actually editing a post when logged in"""
    # Login first
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'admin'

    # Edit the post
    response = client.post('/blog/1/edit', data={
        'title': 'Updated Title',
        'content': 'Updated content',
        'excerpt': 'Updated excerpt',
        'tags': 'updated, test',
        'image_option': 'keep'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Post updated successfully' in response.data
    assert b'Updated Title' in response.data

def test_delete_post_functionality(client):
    """Test actually deleting a post when logged in"""
    # Login first
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'admin'

    # Delete the post
    response = client.post('/blog/1/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Post deleted successfully' in response.data

    # Verify post is gone
    response = client.get('/blog/1')
    assert response.status_code == 404

def test_delete_comment_requires_login(client):
    """Test that deleting comment requires login"""
    # First add a comment
    client.post('/blog/1', data={
        'author': 'Test User',
        'comment_text': 'Test comment'
    })

    # Try to delete without login
    response = client.post('/comment/1/delete', follow_redirects=True)
    assert b'Please log in' in response.data

def test_delete_comment_functionality(client):
    """Test actually deleting a comment when logged in"""
    # Add a comment first
    client.post('/blog/1', data={
        'author': 'Test User',
        'comment_text': 'Test comment to delete'
    })

    # Login
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'admin'

    # Delete the comment
    response = client.post('/comment/1/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Comment deleted successfully' in response.data

def test_norwegian_date_filter(client):
    """Test Norwegian date filter formatting"""
    from app import norwegian_date_filter

    # Test valid date
    result = norwegian_date_filter('2025-12-15')
    assert '15' in result
    assert 'des' in result
    assert '2025' in result

    # Test invalid date returns original
    result = norwegian_date_filter('invalid-date')
    assert result == 'invalid-date'