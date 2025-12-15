# Import Flask
from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Hello, World! My blog is coming soon!"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)