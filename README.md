# Growthzi - AI-Powered Website Builder Backend

This repository contains the backend source code for Growthzi, an AI-driven website builder. The application is built with Python (Flask) and MongoDB, featuring a complete Role-Based Access Control (ACL) system and dynamic content generation via Google's Gemini AI.

## Features

- **User Authentication**: Secure Sign-Up/Login functionality using email and password.
- **JWT-Based Security**: API access is protected using JSON Web Tokens.
- **Role-Based Access Control (ACL)**:
    - Pre-defined roles: `Admin`, `Editor`, `Viewer`.
    - Granular, permission-based access for every API route.
    - Admin-only endpoints for managing user roles.
- **AI Content Generation**: An API endpoint that accepts a business type and industry, and uses Google's Gemini AI to generate a complete JSON structure for a website's content.
- **Full Website CRUD**: API endpoints for creating, reading, updating, and deleting websites, with permissions enforced based on user roles (e.g., Editors can only manage their own websites).
- **Dynamic HTML Preview**: A public-facing route (`/preview/:id`) that renders the generated website content into a live HTML template for immediate preview.

---

## Technology Stack

- **Backend Framework**: **Flask**
- **Database**: **MongoDB**
- **Authentication**: **PyJWT** for JSON Web Tokens, **Werkzeug** for password hashing.
- **AI Service**: **Google Generative AI (Gemini)** for content creation.
- **Python Environment**: `python-dotenv` for managing environment variables.

---

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community) installed and running on your local machine.
- A [Google AI API Key](https://aistudio.google.com/app/apikey) for Gemini.

### 1. Clone the Repository

```bash
git clone https://github.com/Saikumar1801/Growthzi.git
cd Growthzi
```

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project by copying the example file.

```bash
# On macOS/Linux
cp .env.example .env

# On Windows
copy .env.example .env
```

Now, open the `.env` file and fill in your specific configuration details:

```ini
# Flask Configuration
FLASK_APP=run.py
FLASK_DEBUG=True

# MongoDB Connection URI
# For a local instance, this is usually correct.
MONGO_URI="mongodb://localhost:27017/growthzi"

# JWT Secret Key - CHANGE THIS to a long, random string
JWT_SECRET_KEY="your-super-secret-and-long-random-string-for-jwt"

# Google Gemini API Key
GOOGLE_API_KEY="your-google-ai-api-key-here"
```

### 5. Run the Application

Once the setup is complete, you can start the Flask server.

```bash
python run.py
```

The server will start on `http://127.0.0.1:5000`. When you run it for the first time on a fresh database, it will automatically seed the `roles` collection with Admin, Editor, and Viewer roles.

---

## API Usage and Postman

A Postman collection is provided (`Growthzi-API.postman_collection.json`) to demonstrate and test all available API endpoints.

**Initial Admin Setup (Manual Step):**
Since there's no "Sign Up as Admin" feature, you must manually promote the first user.
1. Use the `/api/auth/signup` endpoint to create a new user (e.g., `admin@growthzi.com`).
2. Open a MongoDB client (like MongoDB Compass or `mongosh`).
3. In the `growthzi` database, find the `_id` of the "Admin" role in the `roles` collection.
4. Find your newly created user in the `users` collection and update their `role_id` to match the Admin's `_id`.
5. You can now log in as this user to get an Admin-level JWT and access protected admin routes.
