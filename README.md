# Instagram Clone

## Overview

**Instagram Clone** is a Flask-based web application that mimics key features of Instagram. It offers user authentication with OTP verification during signup, image posting with captions, and a reels page that implements infinite scrolling for video content. The project is designed for educational purposes and is fully deployable on Heroku.

## Features

- **User Authentication:**
  - **Signup:** Users register with full name, email, a unique ID (username), password (with confirmation), and OTP verification.
  - **Login:** Secure login with hashed passwords.
  - **Forgot Password:** Simulated password reset functionality.
  
- **Post Creation:**
  - Users can upload images along with captions.
  - Posts are stored locally in a JSON file (`posts.json`).

- **Reels Scrolling:**
  - A dedicated reels page displays short video clips.
  - Videos are dynamically loaded via JavaScript for a smooth, infinite scroll experience.

- **Deployment Ready:**
  - Includes configuration files like `Procfile`, `requirements.txt`, and an optional `runtime.txt` for deploying on Heroku.
  - Uses Gunicorn as the production web server.

## Folder Structure

/instagram-clone │-- app.py # Main Flask backend │-- requirements.txt # Python dependencies │-- Procfile # Heroku process file │-- runtime.txt # (Optional) Specifies Python version │-- /data # Data storage for JSON files │ │-- users.json # Stores user data (IDs, emails, encrypted passwords) │ │-- posts.json # Stores post details (image filenames and captions) │-- /templates # HTML templates │ │-- index.html # Login page │ │-- signup.html # Signup page (with OTP handling) │ │-- forgot-password.html # Forgot Password page │ │-- home.html # Feed page (post display and uploads) │ │-- reels.html # Reels page (infinite scrolling for videos) │-- /static # Static assets │ │-- style.css # Main CSS file (for all pages) │ │-- scripts.js # JavaScript for the reels page │ │-- /images # Directory for uploaded images │ │-- /videos # Directory for reels videos (MP4 files)

bash
Copy
Edit

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/instagram-clone.git
   cd instagram-clone
Create a Virtual Environment and Install Dependencies:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Run the Application Locally:

bash
Copy
Edit
python app.py
Open your browser and navigate to http://127.0.0.1:5000/ to see the app in action.

Deployment
This application is configured for deployment on Heroku. Follow these steps:

Log in to Heroku CLI:

bash
Copy
Edit
heroku login
Create a New Heroku App:

bash
Copy
Edit
heroku create your-app-name
Deploy Your Code:

bash
Copy
Edit
git push heroku master
(If your branch is named main, use git push heroku main.)

Set Environment Variables (Optional):

For example, to set a secret key:

bash
Copy
Edit
heroku config:set SECRET_KEY="your_secret_key_here"
Open Your Deployed App:

bash
Copy
Edit
heroku open
Your public URL (e.g., https://your-app-name.herokuapp.com/) is now live.

Default Credentials
For testing purposes, a default demo user is automatically created if it doesn’t already exist:

Username: demoUser
Password: Demo@12345
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests. Please open an issue first to discuss what you would like to change.

Acknowledgements
Flask
Heroku
Gunicorn
bcrypt
