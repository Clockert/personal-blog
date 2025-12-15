# Import Flask, render_template, and our database functions
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_all_posts, get_post_by_id, create_post, update_post, delete_post, get_posts_by_tag, get_all_tags, get_comments_for_post, create_comment, delete_comment
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a Flask application
app = Flask(__name__)

# Set secret key for sessions (needed for login)
app.secret_key = os.getenv('SECRET_KEY')

# Get admin credentials from environment
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Home page route
@app.route('/')
def home():
    # Get sort parameter from query string, default to 'date_desc'
    sort_by = request.args.get('sort', 'date_desc')
    posts = get_all_posts(sort_by)
    tags = get_all_tags()
    return render_template('home.html', posts=posts, tags=tags, current_sort=sort_by)

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Individual post route
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found!", 404
    
    # Handle comment submission
    if request.method == 'POST':
        author = request.form.get('author', 'Anonymous')
        comment_text = request.form.get('comment_text')
        
        if comment_text:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d %H:%M')
            create_comment(post_id, author, comment_text, date)
            flash('Comment added successfully!', 'success')
            return redirect(url_for('post', post_id=post_id))
        else:
            flash('Comment cannot be empty', 'error')
    
    # Get comments for this post
    comments = get_comments_for_post(post_id)
    
    return render_template('post.html', post=post, comments=comments)

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Login successful - store in session
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            # Login failed
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

# Create new post route (GET shows form, POST saves post)
@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to create posts', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        content = request.form['content']
        excerpt = request.form['excerpt']
        tags = request.form.get('tags', '')  # Optional field
        image_url = request.form.get('image_url', None)  # Optional field
        
        # Get current date
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d')
        
        # Insert into database
        create_post(title, date, content, excerpt, image_url, tags)
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))
    
    # GET request - show the form with existing tags
    existing_tags = get_all_tags()
    return render_template('new_post.html', existing_tags=existing_tags)

# Edit post route
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to edit posts', 'error')
        return redirect(url_for('login'))
    
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found!", 404
    
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        content = request.form['content']
        excerpt = request.form['excerpt']
        tags = request.form.get('tags', '')
        image_url = request.form.get('image_url', None)
        
        # Keep the original date
        date = post['date']
        
        # Update in database
        update_post(post_id, title, date, content, excerpt, image_url, tags)
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('post', post_id=post_id))
    
    # GET request - show the form with existing data and existing tags
    existing_tags = get_all_tags()
    return render_template('edit_post.html', post=post, existing_tags=existing_tags)

# Delete post route
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post_route(post_id):
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to delete posts', 'error')
        return redirect(url_for('login'))
    
    # Delete the post
    delete_post(post_id)
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('home'))

# Delete comment route
@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment_route(comment_id):
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to delete comments', 'error')
        return redirect(url_for('login'))
    
    # Delete the comment
    delete_comment(comment_id)
    flash('Comment deleted successfully!', 'success')
    
    # Redirect back to the post page
    return redirect(request.referrer or url_for('home'))


# Tag filter route
@app.route('/tag/<tag_name>')
def filter_by_tag(tag_name):
    posts = get_posts_by_tag(tag_name)
    return render_template('tag_filter.html', posts=posts, tag=tag_name)



# Run the application
if __name__ == '__main__':
    app.run(debug=True)