# Import Flask, render_template, and database functions
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_all_posts, get_post_by_id, create_post, update_post, delete_post, get_posts_by_tag, get_all_tags, get_comments_for_post, create_comment, delete_comment, get_posts_count
from validation import validate_post_data, validate_comment_data, validate_image_url, validate_pagination_params, sanitize_tags
import os
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import uuid

# =============================================================================
# Table of Contents
# 1. Configuration and Setup
# 2. Template Filters
# 3. File Upload Helpers
# 4. Authentication Configuration
# 5. Public Routes
# 6. Authentication Routes
# 7. Post Management Routes
# 8. Comment Management Routes
# 9. Tag Filtering Routes
# 10. Application Entry Point
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Configuration and Setup
# -----------------------------------------------------------------------------
# Load environment variables from .env file
load_dotenv()

# Create a Flask application
app = Flask(__name__)

# Set secret key for sessions (needed for login)
app.secret_key = os.getenv('SECRET_KEY')

# Configure file upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# -----------------------------------------------------------------------------
# 2. Template Filters
# -----------------------------------------------------------------------------

# Custom Jinja2 filter for Norwegian date format
@app.template_filter('norwegian_date')
def norwegian_date_filter(date_string):
    """Convert date from YYYY-MM-DD to DD mon YYYY (Norwegian style)"""
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')

        # Norwegian month abbreviations
        norwegian_months = {
            1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'mai', 6: 'jun',
            7: 'jul', 8: 'aug', 9: 'sep', 10: 'okt', 11: 'nov', 12: 'des'
        }

        # Format as DD mon YYYY
        day = date_obj.day
        month = norwegian_months[date_obj.month]
        year = date_obj.year

        return f"{day:02d} {month} {year}"
    except:
        # If parsing fails, return original string
        return date_string

@app.template_filter('norwegian_datetime')
def norwegian_datetime_filter(datetime_string):
    """Convert datetime to DD mon YYYY - HH:MM format (e.g., 17 des 2025 - 14:30)"""
    try:
        dt_obj = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
        norwegian_months = {
            1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'mai', 6: 'jun',
            7: 'jul', 8: 'aug', 9: 'sep', 10: 'okt', 11: 'nov', 12: 'des'
        }
        return f"{dt_obj.day:02d} {norwegian_months[dt_obj.month]} {dt_obj.year} - {dt_obj.hour:02d}:{dt_obj.minute:02d}"
    except:
        return datetime_string

# -----------------------------------------------------------------------------
# 3. File Upload Helpers
# -----------------------------------------------------------------------------

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """Save uploaded file and return the URL path"""
    if file and allowed_file(file.filename):
        # Generate unique filename to avoid collisions
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the file
        file.save(filepath)

        # Return URL path relative to static folder
        return f"/static/uploads/{unique_filename}"
    return None

# -----------------------------------------------------------------------------
# 4. Authentication Configuration
# -----------------------------------------------------------------------------
# Get admin credentials from environment
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')  # Store hashed password in .env

# -----------------------------------------------------------------------------
# 5. Public Routes
# -----------------------------------------------------------------------------
# Landing page route
@app.route('/')
def home():
    """Landing page with hero section and featured posts"""
    # Get the 3 most recent posts for featured section
    featured_posts = get_all_posts(sort_by='date_desc', limit=3)
    return render_template('home.html', featured_posts=featured_posts)

# Blog listing page route
@app.route('/blog')
def blog():
    """Blog listing page with pagination, sorting, and filtering"""
    # Get sort parameter from query string, default to 'date_desc'
    sort_by = request.args.get('sort', 'date_desc')

    # Get page parameter from query string, default to 1
    page = request.args.get('page', 1, type=int)

    # Validate pagination parameters
    is_valid, error_msg, page = validate_pagination_params(page)
    if not is_valid:
        flash(error_msg, 'error')

    # Set posts per page
    per_page = 6

    # Calculate offset
    offset = (page - 1) * per_page

    # Get paginated posts
    posts = get_all_posts(sort_by, limit=per_page, offset=offset)

    # Get total count for pagination
    total_posts = get_posts_count()
    total_pages = (total_posts + per_page - 1) // per_page  # Ceiling division

    tags = get_all_tags()
    return render_template('blog.html',
                         posts=posts,
                         tags=tags,
                         current_sort=sort_by,
                         page=page,
                         total_pages=total_pages)

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# -----------------------------------------------------------------------------
# 6. Authentication Routes
# -----------------------------------------------------------------------------

# Individual blog post route
@app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def blog_post(post_id):
    """Display individual blog post with comments"""
    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found!", 404

    # Handle comment submission
    if request.method == 'POST':
        author = request.form.get('author', 'Anonymous')
        comment_text = request.form.get('comment_text')

        # Validate comment data
        is_valid, error_msg = validate_comment_data(comment_text, author)

        if is_valid:
            date = datetime.now().strftime('%Y-%m-%d %H:%M')
            create_comment(post_id, author, comment_text, date)
            flash('Comment added successfully!', 'success')
            return redirect(url_for('blog_post', post_id=post_id))
        else:
            flash(error_msg, 'error')

    # Get comments for this post
    comments = get_comments_for_post(post_id)

    return render_template('post.html', post=post, comments=comments)

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials - use password hashing for security
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
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

# -----------------------------------------------------------------------------
# 7. Post Management Routes
# -----------------------------------------------------------------------------

# Create new post route (GET shows form, POST saves post)
@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    """Create a new blog post"""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to create posts', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        tags = request.form.get('tags', '')

        # Validate post data
        is_valid, error_msg = validate_post_data(title, content, excerpt, tags)

        if not is_valid:
            flash(error_msg, 'error')
            return render_template('new_post.html', existing_tags=get_all_tags())

        # Sanitize tags
        tags = sanitize_tags(tags)

        # Handle image - either upload or URL
        image_url = None
        image_option = request.form.get('image_option', 'upload')

        if image_option == 'upload':
            # Handle file upload
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file.filename != '':
                    image_url = save_uploaded_file(file)
                    if image_url is None:
                        flash('Invalid file type. Please upload a valid image (PNG, JPG, GIF, WebP).', 'error')
                        return render_template('new_post.html', existing_tags=get_all_tags())
        elif image_option == 'url':
            # Handle URL
            image_url = request.form.get('image_url', '').strip()
            if image_url:
                # Validate image URL
                is_valid_url, url_error_msg = validate_image_url(image_url)
                if not is_valid_url:
                    flash(url_error_msg, 'error')
                    return render_template('new_post.html', existing_tags=get_all_tags())
            else:
                image_url = None

        # Insert into database (timestamps handled automatically)
        create_post(title, content, excerpt, image_url, tags)

        flash('Post created successfully!', 'success')
        return redirect(url_for('blog'))

    # GET request - show the form with existing tags
    existing_tags = get_all_tags()
    return render_template('new_post.html', existing_tags=existing_tags)

# Edit post route
@app.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit an existing blog post"""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to edit posts', 'error')
        return redirect(url_for('login'))

    post = get_post_by_id(post_id)
    if post is None:
        return "Post not found!", 404

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        tags = request.form.get('tags', '')

        # Validate post data
        is_valid, error_msg = validate_post_data(title, content, excerpt, tags)

        if not is_valid:
            flash(error_msg, 'error')
            return render_template('edit_post.html', post=post, existing_tags=get_all_tags())

        # Sanitize tags
        tags = sanitize_tags(tags)

        # Handle image - either upload, URL, or keep existing
        old_image_url = post['image_url']  # Save old image URL for cleanup
        image_url = post['image_url']  # Default to existing image
        image_option = request.form.get('image_option', 'keep')

        if image_option == 'upload':
            # Handle file upload
            if 'image_file' in request.files:
                file = request.files['image_file']
                if file.filename != '':
                    new_image_url = save_uploaded_file(file)
                    if new_image_url:
                        image_url = new_image_url
                        # Delete old uploaded image if it exists
                        if old_image_url and old_image_url.startswith('/static/uploads/'):
                            old_filename = old_image_url.split('/')[-1]
                            old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
                            if os.path.exists(old_filepath):
                                try:
                                    os.remove(old_filepath)
                                except Exception as e:
                                    print(f"Error deleting old image: {e}")
                    else:
                        flash('Invalid file type. Please upload a valid image (PNG, JPG, GIF, WebP).', 'error')
                        return render_template('edit_post.html', post=post, existing_tags=get_all_tags())
        elif image_option == 'url':
            # Handle URL
            image_url = request.form.get('image_url', '').strip()
            if image_url:
                # Validate image URL
                is_valid_url, url_error_msg = validate_image_url(image_url)
                if not is_valid_url:
                    flash(url_error_msg, 'error')
                    return render_template('edit_post.html', post=post, existing_tags=get_all_tags())
                # Delete old uploaded image if switching to URL
                if image_url != old_image_url and old_image_url and old_image_url.startswith('/static/uploads/'):
                    old_filename = old_image_url.split('/')[-1]
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
                    if os.path.exists(old_filepath):
                        try:
                            os.remove(old_filepath)
                        except Exception as e:
                            print(f"Error deleting old image: {e}")
            else:
                image_url = None
                # Delete old uploaded image if removing image
                if old_image_url and old_image_url.startswith('/static/uploads/'):
                    old_filename = old_image_url.split('/')[-1]
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
                    if os.path.exists(old_filepath):
                        try:
                            os.remove(old_filepath)
                        except Exception as e:
                            print(f"Error deleting old image: {e}")
        # If image_option == 'keep', image_url stays as post['image_url']

        # Keep the original date
        date = post['date']

        # Update in database
        update_post(post_id, title, date, content, excerpt, image_url, tags)

        flash('Post updated successfully!', 'success')
        return redirect(url_for('blog_post', post_id=post_id))

    # GET request - show the form with existing data and existing tags
    existing_tags = get_all_tags()
    return render_template('edit_post.html', post=post, existing_tags=existing_tags)

# Delete post route
@app.route('/blog/<int:post_id>/delete', methods=['POST'])
def delete_post_route(post_id):
    """Delete a blog post and its associated uploaded image"""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to delete posts', 'error')
        return redirect(url_for('login'))

    # Get the post to check for uploaded image
    post = get_post_by_id(post_id)
    if post and post['image_url']:
        # Check if it's an uploaded file (starts with /static/uploads/)
        if post['image_url'].startswith('/static/uploads/'):
            # Extract filename and delete the file
            filename = post['image_url'].split('/')[-1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    # Log error but continue with post deletion
                    print(f"Error deleting image file: {e}")

    # Delete the post
    delete_post(post_id)

    flash('Post deleted successfully!', 'success')
    return redirect(url_for('blog'))

# -----------------------------------------------------------------------------
# 8. Comment Management Routes
# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
# 9. Tag Filtering Routes
# -----------------------------------------------------------------------------

# Tag filter route
@app.route('/tag/<tag_name>')
def filter_by_tag(tag_name):
    posts = get_posts_by_tag(tag_name)
    return render_template('tag_filter.html', posts=posts, tag=tag_name)

# -----------------------------------------------------------------------------
# 10. Application Entry Point
# -----------------------------------------------------------------------------
# Run the application
if __name__ == '__main__':
    # If you run this file directly, start the Flask development server
    app.run(debug=True)
