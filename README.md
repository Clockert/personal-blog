# Personal Blog

A blogging application I'm building for my Backend Essentials course project. Learning to build a full backend system with Flask and SQLite.

## What I'm Building

A blog where I can:
- Write and publish blog posts
- Add comments to posts
- Organize posts with tags
- Edit existing posts
- Secure admin access with login

This project is helping me practice backend development, database management, and writing secure code.

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

### 🔄 Phase 4: Creating Content (In Progress)
- [ ] "New Post" button (visible when logged in)
- [ ] Form to create blog posts
- [ ] Handle form submission
- [ ] Insert new posts into database
- [ ] Form validation

### 📋 Phase 5: Editing & Tags (Planned)
- [ ] Edit existing posts
- [ ] Update posts in database
- [ ] Tag filtering page
- [ ] Attach/manage tags

### 🧪 Phase 6: Security & Testing (Planned)
- [ ] Input validation and sanitization
- [ ] Parameterized queries (SQL injection prevention)
- [ ] HTML escaping (XSS prevention)
- [ ] Integration tests
- [ ] End-to-end tests

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
│   ├── base.html        # Base template
│   ├── home.html        # Home page
│   ├── post.html        # Individual post
│   └── login.html       # Login page
├── static/
│   └── style.css        # Styling
└── tests/               # Tests (coming soon)
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

**Phase:** 4 - Creating Content (In Progress)

**What's Working:**
- Full blog reading experience
- User authentication system
- Dynamic routing and navigation
- Tag display
- Database-driven content

**What I'm Working On:**
- Building the "Create New Post" form
- Protecting routes to require login

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

*(These are documented in more detail in my reflective journal)*

### Terminal Navigation
- **Challenge:** Not comfortable with terminal commands - usually use GUI tools
  - **Solution:** Learned that VS Code has an integrated terminal that opens directly in my project folder. Started with just a few essential commands: `python app.py`, `source venv/bin/activate`, and `python`. Getting more comfortable with practice.

### Understanding Flask's Request-Response Cycle
- **Challenge:** Understanding how `@app.route()` connects URLs to Python functions
  - **Solution:** Started with simplest possible "Hello World", then gradually added complexity. Drawing out the flow helped: Browser → Flask route → Python function → Template → Browser

### Moving from Hardcoded Data to Database
- **Challenge:** Had working code with Python lists, felt risky to change everything
  - **Solution:** Used Git branches! Created `add-database` branch so I could experiment without breaking working code. Could always go back if needed. This made me feel safe to try new things.

### Python Interactive Shell for Database
- **Challenge:** Adding data to database using Python shell was confusing - didn't understand the `>>>` prompt
  - **Solution:** Realized the Python shell is just typing Python commands one at a time instead of in a file. Used it to test database queries before adding them to my code.

### Git Workflow with Branches
- **Challenge:** At first added features directly to main, then learned I should use branches
  - **Solution:** Started creating branches for major features. Made one mistake and added tags to main instead of a branch - learned from it! Now more comfortable with branch → develop → merge workflow.

### Sessions and Login State
- **Challenge:** Understanding how Flask "remembers" that I'm logged in between page loads
  - **Solution:** Learned that sessions store data in encrypted cookies. The `session['logged_in']` is stored in the browser and sent with each request. This clicked when I saw the logout function removing it from the session.

### Environment Variables and Security
- **Challenge:** Wasn't sure why we needed a separate .env file
  - **Solution:** Realized that if I push my code to GitHub, everyone could see my password if it's in the code! .env file + .gitignore keeps secrets local. This is important for real-world projects.

## Future Enhancements

If time permits:
- Comment system
- Delete functionality
- Advanced tag filtering
- Rich text editor
- Search functionality
- Multiple users

## Course Information

Backend Essentials - Project Assignment
Building a personal blogging application from scratch

---

*Last Updated: December 2024*
