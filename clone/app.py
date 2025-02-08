from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json, os, bcrypt, random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure secret key

# Define folders for data and uploads
DATA_FOLDER = "data"
UPLOAD_FOLDER = "static/images"
REELS_FOLDER = "static/videos"
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REELS_FOLDER, exist_ok=True)

# Data file paths
users_file = os.path.join(DATA_FOLDER, "users.json")
posts_file = os.path.join(DATA_FOLDER, "posts.json")

# Initialize users.json if it doesn't exist
if not os.path.exists(users_file):
    with open(users_file, "w") as f:
        json.dump({}, f)

# Initialize posts.json if it doesn't exist
if not os.path.exists(posts_file):
    with open(posts_file, "w") as f:
        json.dump([], f)

# Optionally, create a default demo user (for testing)
with open(users_file, "r") as f:
    users = json.load(f)
if "demoUser" not in users:
    default_password = "Demo@12345"
    hashed_pw = bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    users["demoUser"] = {
        "fullname": "Demo User",
        "email": "demo@example.com",
        "password": hashed_pw
    }
    with open(users_file, "w") as f:
        json.dump(users, f)

# Signup route with OTP verification
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # OTP verification step
        if "otp" in request.form:
            entered_otp = request.form["otp"]
            pending_data = session.get("pending_signup")
            if not pending_data:
                flash("No pending signup data found. Please try again.", "danger")
                return redirect(url_for("signup"))
            if entered_otp == session.get("signup_otp"):
                # OTP correct; register user
                fullname = pending_data.get("fullname", "")
                email = pending_data["email"]
                username = pending_data["username"]
                password = pending_data["password"]

                # Load existing users
                with open(users_file, "r") as f:
                    users = json.load(f)
                if username in users:
                    flash("Username already exists!", "danger")
                    session.pop("pending_signup", None)
                    session.pop("signup_otp", None)
                    return redirect(url_for("signup"))

                # Encrypt password and save user
                hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                users[username] = {"fullname": fullname, "email": email, "password": hashed_pw}
                with open(users_file, "w") as f:
                    json.dump(users, f)

                flash("Signup successful! You can now log in.", "success")
                session.pop("pending_signup", None)
                session.pop("signup_otp", None)
                return redirect(url_for("login"))
            else:
                flash("Incorrect OTP. Please try again.", "danger")
                return redirect(url_for("signup"))
        else:
            # Initial signup submission
            fullname = request.form.get("fullname", "")
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            if password != confirm_password:
                flash("Passwords do not match!", "danger")
                return redirect(url_for("signup"))

            with open(users_file, "r") as f:
                users = json.load(f)
            if username in users:
                flash("Username already exists!", "danger")
                return redirect(url_for("signup"))

            # Generate OTP (simulate sending via email)
            otp = str(random.randint(100000, 999999))
            session["pending_signup"] = {
                "fullname": fullname,
                "email": email,
                "username": username,
                "password": password
            }
            session["signup_otp"] = otp

            # In a production app, send the OTP via email.
            # For demo purposes, display the OTP as a flash message.
            flash(f"OTP sent to {email} (Demo OTP is {otp})", "info")
            return render_template("signup.html", otp_required=True)
    else:
        otp_required = "pending_signup" in session
        return render_template("signup.html", otp_required=otp_required)

# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open(users_file, "r") as f:
            users = json.load(f)
        if username not in users or not bcrypt.checkpw(password.encode("utf-8"), users[username]["password"].encode("utf-8")):
            flash("Invalid username or password!", "danger")
            return redirect(url_for("login"))
        session["username"] = username
        flash("Login successful!", "success")
        return redirect(url_for("home"))
    return render_template("index.html")

# Home route – display posts and allow uploads
@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    with open(posts_file, "r") as f:
        posts = json.load(f)
    return render_template("home.html", posts=posts, username=session["username"])

# Logout route
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# Forgot password route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        flash("Password reset link sent to your email.", "info")
        return redirect(url_for("login"))
    return render_template("forgot-password.html")

# Post upload route
@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))
    file = request.files["image"]
    caption = request.form["caption"]
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        with open(posts_file, "r") as f:
            posts = json.load(f)
        posts.append({"username": session["username"], "image": filename, "caption": caption})
        with open(posts_file, "w") as f:
            json.dump(posts, f)
    flash("Post uploaded successfully!", "success")
    return redirect(url_for("home"))

# Reels API route – returns list of video files (MP4)
@app.route("/reels")
def reels_api():
    videos = [f for f in os.listdir(REELS_FOLDER) if f.endswith(".mp4")]
    return jsonify(videos)

if __name__ == "__main__":
    app.run(debug=True)
