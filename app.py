# Import Flask and render_template
from flask import Flask, render_template

# Create a Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    # Render the home.html template
    return render_template('home.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)