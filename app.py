from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "posts.json"

# ---------- helpers ----------
def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def next_id(posts):
    return max((p["id"] for p in posts), default=0) + 1

# ---------- pages ----------
@app.route("/")
def index():
    posts = load_posts()
    posts.sort(key=lambda p: p["created"], reverse=True)
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def view_post(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return redirect(url_for("index"))
    return render_template("post.html", post=post)

# ---------- API ----------
@app.route("/api/posts", methods=["GET"])
def api_get_posts():
    posts = load_posts()
    posts.sort(key=lambda p: p["created"], reverse=True)
    return jsonify(posts)

@app.route("/api/posts", methods=["POST"])
def api_create_post():
    data = request.json
    posts = load_posts()
    post = {
        "id": next_id(posts),
        "title": data.get("title", "").strip(),
        "content": data.get("content", "").strip(),
        "author": data.get("author", "Anonymous").strip() or "Anonymous",
        "category": data.get("category", "General").strip() or "General",
        "created": datetime.now().isoformat(),
        "created_display": datetime.now().strftime("%d %b %Y"),
        "likes": 0,
        "comments": []
    }
    if not post["title"] or not post["content"]:
        return jsonify({"error": "Title and content are required"}), 400
    posts.append(post)
    save_posts(posts)
    return jsonify(post), 201

@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def api_update_post(post_id):
    data = request.json
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"]).strip()
            post["content"] = data.get("content", post["content"]).strip()
            post["category"] = data.get("category", post["category"]).strip()
            post["updated"] = datetime.now().strftime("%d %b %Y")
            save_posts(posts)
            return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def api_delete_post(post_id):
    posts = load_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    return jsonify({"success": True})

@app.route("/api/posts/<int:post_id>/like", methods=["POST"])
def api_like_post(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            save_posts(posts)
            return jsonify({"likes": post["likes"]})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/posts/<int:post_id>/comment", methods=["POST"])
def api_comment(post_id):
    data = request.json
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            comment = {
                "author": data.get("author", "Anonymous").strip() or "Anonymous",
                "text": data.get("text", "").strip(),
                "date": datetime.now().strftime("%d %b %Y")
            }
            if not comment["text"]:
                return jsonify({"error": "Comment cannot be empty"}), 400
            post.setdefault("comments", []).append(comment)
            save_posts(posts)
            return jsonify(comment), 201
    return jsonify({"error": "Post not found"}), 404

# ---------- run ----------
if __name__ == "__main__":
    print("\n✅  Mini Blog is running!")
    print("🌐  Open: http://localhost:5000")
    print("⏹   Press CTRL+C to stop\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
