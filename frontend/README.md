# Growthzi AI Website Builder - Frontend

This is the React frontend for the Growthzi AI Website Builder. It provides a user dashboard for managing websites and an admin panel for user management.

## Prerequisites

- Node.js and npm (or yarn) installed.
- The Flask backend server must be running (typically on `http://127.0.0.1:5000`).

## Setup and Installation

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```
    This will install React, React Router, Axios, and other necessary packages.

3.  **Start the development server:**
    ```bash
    npm start
    ```
    This runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser. The page will reload when you make changes.

## Features

-   **Authentication**: Secure signup and login for users.
-   **Dashboard**: A central place to view and manage all your websites.
-   **AI Website Generation**: Create a new website simply by providing a business type and industry.
-   **Website Editor**: A form-based editor to update the content of your websites.
-   **Live Preview**: Instantly view your website on a public URL.
-   **Role-Based Access Control**: The UI adapts based on user roles (Admin, Editor). Admins have access to an exclusive admin panel.
-   **Admin Panel**: Allows administrators to assign roles to other users.

## How It Works

-   **API Communication**: Uses `axios` to make requests to the Flask backend. An interceptor automatically attaches the JWT authentication token to every request after login.
-   **State Management**: Uses React's Context API (`AuthContext`) to manage global authentication state, making user data and roles available throughout the application.
-   **Routing**: Uses `react-router-dom` for all client-side routing, including private routes that require authentication. 
