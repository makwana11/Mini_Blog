# 📰 The Inkwell — Mini Blog with Flask

A beautiful, fully functional blog app built with Python (Flask).
Write posts, comment, like, filter by category, and more!

---

## 🗂 Project Structure

mini_blog/
├── app.py              ← Flask backend (run this)
├── requirements.txt    ← Python dependencies
├── posts.json          ← Auto-created when you publish posts
└── templates/
    └── index.html      ← Full frontend UI

---

## 🚀 How to Run in VS Code

### Step 1 — Open Folder
File → Open Folder → select the mini_blog folder

### Step 2 — Open Terminal
Press Ctrl + ` (backtick)

### Step 3 — Install Flask
  pip install flask

### Step 4 — Run the App
  python app.py

### Step 5 — Open in Browser
  http://localhost:5000

---

## ✨ Features
- Write & publish blog posts
- Edit and delete posts
- Like posts (tracked per browser)
- Comment on any post
- Filter by category (Tech, Life, Travel, Food, General)
- Hero section shows latest post
- Live sidebar stats (posts, likes, comments, authors)
- Posts saved to posts.json (persists after restart)

---

## 🤝 2-Person Use
Both people can run the app on the same machine,
OR share over local network:
- Find your IP: run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Partner opens: http://YOUR_IP:5000

---

## ❓ Troubleshooting
- "No module named flask" → run: pip install flask
- Port in use → change port=5000 to port=5001 in app.py
- Posts not saving → make sure you're running from inside the mini_blog folder
