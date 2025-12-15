# 📝 Personal Blog Project

A blogging application I'm building for my Backend Essentials course. Here I'm learning to create a full backend using Flask + SQLite.

---

## 🚧 What I'm Building

A simple blog where I can:

- ✍️ Write and publish blog posts
- 💬 Add comments to posts
- 🏷️ Organize posts with tags
- ✏️ Edit existing posts

This project helps me practice backend development, database design, and secure coding 🔐.

---

## 📅 Development Roadmap

I'm building this step-by-step — starting simple, adding features gradually.

### ✅ Phase 0: Foundation _(Complete!)_

- [x] 📁 Set up project structure
- [x] 🐍 Create virtual environment
- [x] 🔧 Install Flask
- [x] 👋 Build "Hello World" app
- [x] 📌 First git commit

### 🎨 Phase 1: Static Templates _(Next)_

- [ ] 🧱 Create basic HTML templates
- [ ] 🎨 Add CSS styling
- [ ] 📝 Display hardcoded posts via Jinja2
- [ ] 🔀 Learn routing

### 🗄️ Phase 2: Database

- [ ] 🧩 Design database schema
- [ ] 🧪 Write SQL to create tables
- [ ] 🗃️ Build database.py
- [ ] 🌱 Add sample data
- [ ] 🔌 Connect templates to database

### 👀 Phase 3: Viewing Posts

- [ ] 🏠 Display all posts on home page
- [ ] 📄 Show individual post pages
- [ ] 💬 Display comments
- [ ] 🧭 Add navigation

### ✍️ Phase 4: Creating Content

- [ ] ➕ Add form for new posts
- [ ] 📬 Handle form submissions
- [ ] ✔️ Validate forms
- [ ] 💭 Add comment form

### 🔧 Phase 5: Editing & Tags

- [ ] ✏️ Edit existing posts
- [ ] 🏷️ Add tag system
- [ ] 🔍 Filter posts by tag

### 🔒 Phase 6: Security & Testing

- [ ] ✔️ Input validation
- [ ] 🛡️ Prevent SQL injection
- [ ] 🚫 Prevent XSS
- [ ] 🧪 Write tests

---

## 🛠️ Technologies

- 🐍 **Flask** - Python web framework
- 🗄️ **SQLite** - Database
- 🧩 **Jinja2** - Template engine
- 🌱 **Git/GitHub** - Version control

---

## 📁 Project Structure

```
personal-blog/
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── home.html
│   └── post.html
├── static/
│   └── style.css
└── tests/
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone [repo-url]
cd personal-blog
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

👉 **Visit:** http://localhost:5000

---

## 📊 Current Status

**Phase:** 0 – Foundation Complete 🎉

**✅ What's working:**

- Basic Flask app that displays Hello World

**🔜 What's next:**

- Creating my first templates (base.html, home.html, post.html)

---

## 📘 Learning Notes

Things I want to remember:

- ⚡ Always activate venv: `source venv/bin/activate`
- 🔀 `@app.route()` decides which function runs for a URL
- 🐞 `debug=True` is great for development — never for production

---

## 🤯 Challenges I've Faced

_(To be documented — great material for my reflective journal!)_

---

## 🌟 Future Ideas

If I have extra time, I might add:

- 🔐 User login system
- 🗑️ Delete posts/comments
- 🔎 Search functionality
- ✍️ Better rich-text editor

---

## 🎓 Course Info

**Backend Essentials** – Project Assignment
Building a personal blogging application from scratch.
