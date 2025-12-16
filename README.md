# Personal Blog

A blogging application I'm building for my Backend Essentials course project. Learning to build a full backend system with Flask and SQLite.

## What I'm Building

A fully-featured blog with:

- Write, edit, and delete blog posts
- Intelligent image management with automatic cleanup
- Comment system with author names
- Tag organization and filtering
- Post sorting and pagination
- Multiple image options (upload or URL)
- Secure admin authentication
- Separate landing page and blog listing
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

- **Backend:** Flask 3.1.2 (Python)
- **Database:** SQLite3
- **Templates:** Jinja2
- **Testing:** pytest 9.0.2
- **Environment Management:** python-dotenv 1.0.1
- **Version Control:** Git/GitHub
- **Security:** Flask sessions, environment variables

## Key Features

### Server-Side Input Validation

- **Comprehensive validation**: All user inputs validated before database operations
- **Security-first approach**: Prevents empty posts, extremely long content, and malicious URLs
- **Length limits**:
  - Titles: max 200 characters
  - Content: max 50,000 characters
  - Comments: max 5,000 characters
  - Tags: max 20 tags, auto-deduplicated
- **URL validation**: Image URLs must use http/https protocol (prevents file:// attacks)
- **Pagination protection**: Page numbers validated to prevent negative or extreme values
- **User-friendly errors**: Clear error messages guide users to fix invalid input
- **39 validation tests**: Comprehensive test coverage ensures reliability

### Intelligent Image Management

- **Multiple input options**: Upload files or provide image URLs
- **Automatic cleanup**: Uploaded images are automatically deleted when:
  - A post is deleted
  - An image is replaced with a new one during editing
  - Switching from uploaded image to URL
- **Unique filenames**: UUID-based naming prevents filename collisions
- **File validation**: Supports PNG, JPG, JPEG, GIF, WebP (max 5MB)
- **Safe storage**: All uploads stored in dedicated `static/uploads/` directory

### Content Organization

- **Pagination**: Blog posts displayed 6 per page with page navigation
- **Flexible sorting**: Sort posts by newest, oldest, or alphabetical
- **Tag system**: Filter posts by tags, with tag suggestions in forms
- **Dual page structure**:
  - Landing page with hero section and 3 featured posts
  - Separate blog listing page with full pagination

### Comments System

- **Public commenting**: Anyone can leave comments (no login required)
- **Anonymous support**: Comments default to "Anonymous" if no name provided
- **Admin moderation**: Only logged-in admins can delete comments
- **Timestamps**: Automatic date/time stamping for all comments

### Security & Authentication

- **Password hashing**: Passwords secured using PBKDF2-SHA256 with 1,000,000 iterations
  - Never stores plaintext passwords
  - Uses `werkzeug.security` for industry-standard hashing
  - Includes random salt to prevent rainbow table attacks
  - Generate new hashes with: `python generate_password_hash.py`
- **Server-side validation**: All inputs validated to prevent data corruption and DoS attacks
- **Protected routes**: Admin-only access for creating, editing, and deleting content
- **Session management**: Flask sessions for secure login state
- **Environment variables**: Sensitive credentials stored safely in `.env` file
- **Flash messages**: User feedback for all actions (success/error states)
- **SQL injection prevention**: Parameterized queries throughout the application

## Project Structure

```
personal-blog/
├── app.py                 # Main Flask application
├── database.py            # Database functions
├── validation.py          # Input validation functions
├── generate_password_hash.py  # Password hash generator utility
├── schema.sql             # Database schema
├── blog.db               # SQLite database
├── .env                  # Environment variables (not in git)
├── requirements.txt      # Python dependencies
├── SECURITY.md           # Security policy and guidelines
├── templates/
│   ├── base.html        # Base template with header/footer
│   ├── home.html        # Home page with posts list
│   ├── blog.html        # Blog posts listing page
│   ├── post.html        # Individual post with comments
│   ├── login.html       # Login page
│   ├── new_post.html    # Create new post form
│   ├── edit_post.html   # Edit post form
│   ├── tag_filter.html  # Filtered posts by tag
│   ├── about.html       # About page
│   └── 404.html         # Custom 404 error page
├── static/
│   ├── style.css        # Complete styling system
│   ├── logo.png         # Blog logo
│   └── uploads/         # Uploaded images for posts
├── tests/
│   ├── test_app.py      # Flask application tests (13 tests)
│   ├── test_database.py # Database function tests (7 tests)
│   └── test_validation.py # Input validation tests (39 tests)
├── venv/                 # Virtual environment (not in git)
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
git clone https://github.com/Clockert/personal-blog.git
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

Create a `.env` file with:

```bash
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your-hashed-password-here
```

**To generate a password hash:**

```bash
python generate_password_hash.py
# Enter your password when prompted
# Copy the hash to your .env file
```

## Testing

The project includes comprehensive automated tests with **59 total tests** covering the Flask application, database operations, and input validation.

### Running Tests

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run all tests (59 tests)
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_app.py         # 13 tests
pytest tests/test_database.py    # 7 tests
pytest tests/test_validation.py  # 39 tests

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Test Structure

- **test_app.py** - Tests for Flask routes, authentication, CRUD operations, and error handling (13 tests)
- **test_database.py** - Tests for database functions including post creation, retrieval, updates, and tag management (7 tests)
- **test_validation.py** - Comprehensive tests for input validation functions (39 tests)
  - Post data validation (title, content, excerpt, tags)
  - Comment validation (text length, author length)
  - Image URL validation (protocol checking, length limits)
  - Pagination parameter validation (bounds checking)
  - Tag sanitization (deduplication, whitespace removal, limits)

## Current Status

**Phase:** Complete! All planned features implemented

**Features:**

- ✅ **Password hashing** with PBKDF2-SHA256 (industry-standard security)
- ✅ **Server-side input validation** with comprehensive security checks
- ✅ Full CRUD operations (Create, Read, Update, Delete) for posts
- ✅ Intelligent image management with automatic cleanup on delete/replace
- ✅ Multiple image options (file upload with 5MB limit or URL validation)
- ✅ Comment system with anonymous support and admin moderation
- ✅ Tag-based filtering and organization with suggestions
- ✅ Post pagination (6 posts per page) and sorting (newest/oldest/alphabetical)
- ✅ Dual page structure (landing page with hero + blog listing)
- ✅ User authentication with protected routes
- ✅ Norwegian date formatting (DD mon YYYY)
- ✅ UUID-based unique filename generation for uploads
- ✅ Custom 404 error handling
- ✅ About page
- ✅ Responsive UI
- ✅ Flash messages for user feedback
- ✅ Automated testing with pytest (59 tests, 100% passing)

## Potential Future Enhancements

Ideas for further development:

- Rich text editor for markdown support
- Search functionality across posts
- Multiple user roles (admin, editor, viewer)
- Post drafts and scheduling
- Comment replies/threading
- Email notifications
- Post categories (in addition to tags)
- Image compression and optimization
- Better design and personalization

## Course Information

Backend Essentials - Project Assignment
Building a personal blogging application

---

_Last Updated: December 2025_
