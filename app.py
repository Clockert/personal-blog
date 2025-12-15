# Import Flask and render_template
from flask import Flask, render_template

# Create a Flask application
app = Flask(__name__)

# Blog posts data - stored as a list of dictionaries
posts = [
    {
        'id': 1,
        'title': 'My First Blog Post',
        'date': 'December 15, 2024',
        'content': 'This is my first blog post! I\'m learning Flask and building this blog from scratch. It\'s exciting to see everything come together. I\'m starting to understand how the backend connects to the frontend.',
        'excerpt': 'This is my first blog post! I\'m learning Flask and building this blog from scratch.'
    },
    {
        'id': 2,
        'title': 'Learning Backend Development',
        'date': 'December 14, 2024',
        'content': 'Today I\'m working on understanding how Flask routing works and how to render templates. The concepts are starting to click! It\'s amazing how Python can generate dynamic HTML.',
        'excerpt': 'Today I\'m working on understanding how Flask routing works and how to render templates.'
    },
    {
        'id': 3,
        'title': 'Understanding Jinja2 Templates',
        'date': 'December 13, 2024',
        'content': 'Jinja2 is really powerful! I can now pass data from Python to my HTML templates and use loops and conditionals to display content dynamically. This is much better than hardcoding everything in HTML.',
        'excerpt': 'Jinja2 is really powerful! I can now pass data from Python to my HTML templates.'
    },
    {
    'id': 4,
    'title': 'Your title here',
    'date': 'December 12, 2024',
    'content': 'Your full content here...',
    'excerpt': 'Your short excerpt here...'
}
]

# Define a route for the home page
@app.route('/')
def home():
    # Pass the posts data to the template
    return render_template('home.html', posts=posts)

# Define a route for individual posts
# <int:post_id> means this part of the URL will be a number
@app.route('/post/<int:post_id>')
def post(post_id):
    # Find the post with matching id
    post = None
    for p in posts:
        if p['id'] == post_id:
            post = p
            break
    
    # If post not found, show error message
    if post is None:
        return "Post not found!", 404
    
    # Render the post template with the found post
    return render_template('post.html', post=post)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)