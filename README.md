# Personal Blog

A blogging application I'm building for my Backend Essentials course project. Learning to build a full backend system with Flask and SQLite.

## What I'm Building

A fully-featured blog with:

- Write, edit, and delete blog posts
- Comment system with author names
- Tag organization and filtering
- Post sorting (date/title)
- Image support for posts
- Secure admin authentication
- Norwegian date formatting
- Custom 404 error page
- About page

This project helped me practice backend development, database management, and writing secure code.

## Development Progress

Building this incrementally, starting simple and adding features step by step.

### ✅ Phase 0: Foundation (Complete!)

- [x] Set up project structure
- [x] Create virtual environment
- [x] Install Flask
- [x] Build "Hello World" Flask app
- [x] First git commit

### ✅ Phase 1: Static Templates (Complete!)

- [x] Create base template with Jinja2 blocks
- [x] Build home page template
- [x] Build individual post template
- [x] Add CSS styling with custom design system
- [x] Display hardcoded posts using loops

### ✅ Phase 2: Database (Complete!)

- [x] Design database schema
- [x] Create schema.sql file
- [x] Build database.py module with query functions
- [x] Migrate from hardcoded data to SQLite
- [x] Add sample posts to database

### ✅ Phase 3: Reading Posts (Complete!)

- [x] Display all posts on home page (newest first)
- [x] Individual post pages with full content
- [x] Working navigation between pages
- [x] Tag display on posts
- [x] Dynamic routing with post IDs

### ✅ Login System (Complete!)

- [x] User authentication with Flask sessions
- [x] Login/logout functionality
- [x] Protected routes
- [x] Flash messages for user feedback
- [x] Environment variables for credentials

### ✅ Phase 4: Creating Content (Complete!)

- [x] "New Post" button (visible when logged in)
- [x] Form to create blog posts
- [x] Handle form submission
- [x] Insert new posts into database
- [x] Form validation

### ✅ Phase 5: Editing & Tags (Complete!)

- [x] Edit existing posts
- [x] Update posts in database
- [x] Delete posts functionality
- [x] Tag filtering page
- [x] Attach/manage tags
- [x] Browse tags section

### ✅ Phase 6: Comments System (Complete!)

- [x] Comment form on post pages
- [x] Display comments with timestamps
- [x] Delete comments (admin only)
- [x] Comment author field

### ✅ Phase 7: Enhancements (Complete!)

- [x] Post sorting (newest/oldest/alphabetical)
- [x] Norwegian date formatting
- [x] About page
- [x] Custom 404 page
- [x] Post images support
- [x] Tag suggestions in forms
- [x] Improved UI/UX

## Technologies Used

- **Backend:** Flask (Python)
- **Database:** SQLite3
- **Templates:** Jinja2
- **Version Control:** Git/GitHub
- **Security:** Flask sessions, environment variables

## Project Structure

```
personal-blog/
├── app.py                 # Main Flask application
├── database.py            # Database functions
├── schema.sql             # Database schema
├── blog.db               # SQLite database
├── .env                  # Environment variables (not in git)
├── requirements.txt      # Python dependencies
├── templates/
│   ├── base.html        # Base template with header/footer
│   ├── home.html        # Home page with posts list
│   ├── post.html        # Individual post with comments
│   ├── login.html       # Login page
│   ├── new_post.html    # Create new post form
│   ├── edit_post.html   # Edit post form
│   ├── tag_filter.html  # Filtered posts by tag
│   ├── about.html       # About page
│   └── 404.html         # Custom 404 error page
├── static/
│   ├── style.css        # Complete styling system
│   └── logo.png         # Blog logo
└── .gitignore           # Git ignore file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd personal-blog

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
# SECRET_KEY=your-secret-key
# ADMIN_USERNAME=admin
# ADMIN_PASSWORD=your-password

# Initialize database
python database.py

# Run the application
python app.py
```

Visit `http://localhost:5000`

### Login Credentials

Set these in your `.env` file (see `.env.example`)

## Current Status

**Phase:** Complete! All planned features implemented

**Features:**

- ✅ Full CRUD operations (Create, Read, Update, Delete) for posts
- ✅ Comment system with delete functionality
- ✅ Tag-based filtering and organization
- ✅ Post sorting (newest/oldest/alphabetical)
- ✅ User authentication with protected routes
- ✅ Norwegian date formatting (DD mon YYYY)
- ✅ Image support for blog posts
- ✅ Custom 404 error handling
- ✅ About page
- ✅ Responsive UI
- ✅ Flash messages for user feedback

## Learning Notes

Key things I've learned:

- Virtual environments keep project dependencies isolated
- `@app.route()` decorator maps URLs to Python functions
- Jinja2 templates let you separate logic from presentation
- SQLite is lightweight but powerful for small projects
- Sessions track user state across requests
- Environment variables protect sensitive data
- Git branches help organize feature development

## Challenges & Solutions

_(These are documented in more detail in my reflective journal)_

### Terminal Navigation

- **Challenge:** Not comfortable with terminal commands - usually use GUI tools
  - **Solution:** Started to use VS Codes integrated terminal that opens directly in my project folder. Started with just a few essential commands: `python app.py`, `source venv/bin/activate`, and `python`. Getting more comfortable with practice.

### Understanding Flask's Request-Response Cycle

- **Challenge:** Understanding how `@app.route()` connects URLs to Python functions
  - **Solution:** Started with simplest possible "Hello World", then gradually added complexity. Drawing out the flow helped: Browser → Flask route → Python function → Template → Browser

### Moving from Hardcoded Data to Database

- **Challenge:** Had working code with Python lists, felt scary to change everything
  - **Solution:** Used Git branches, Created `add-database` branch so I could experiment without breaking working code. Could always go back if needed. This made me feel safe to try new things.

### Python Interactive Shell for Database

- **Challenge:** Adding data to database using Python shell was confusing - didn't fully understand the `>>>` prompt
  - **Solution:** Realized the Python shell is just typing Python commands one at a time instead of in a file. Used it to test database queries before adding them to my code.

### Sessions and Login State

- **Challenge:** Understanding how Flask "remembers" that I'm logged in between page loads
  - **Solution:** Learned that sessions store data in encrypted cookies. The `session['logged_in']` is stored in the browser and sent with each request. This clicked when I saw the logout function removing it from the session.

## Potential Future Enhancements

Ideas for further development:

- Rich text editor for markdown support
- More options for images
- Search functionality across posts
- Multiple user roles (admin, editor, viewer)
- Post drafts and scheduling
- Comment replies/threading
- Email notifications
- Post categories (in addition to tags)
- Better Design and personalisation

## Course Information

Backend Essentials - Project Assignment
Building a personal blogging application

---

_Last Updated: December 2025_
