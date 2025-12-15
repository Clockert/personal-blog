# Import Flask, render_template, and our database functions
from flask import Flask, render_template
from database import get_all_posts, get_post_by_id

# Create a Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    # Get posts from database instead of hardcoded list
    posts = get_all_posts()
    return render_template('home.html', posts=posts)

# Define a route for individual posts
@app.route('/post/<int:post_id>')
def post(post_id):
    # Get post from database
    post = get_post_by_id(post_id)
    
    # If post not found, show error message
    if post is None:
        return "Post not found!", 404
    
    # Render the post template with the found post
    return render_template('post.html', post=post)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)