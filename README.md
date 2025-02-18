# Merchandise Inventory Management

## Overview
This project is a Merchandise Inventory Management application that includes a FastAPI backend and a React frontend. The application allows users to register, log in, and manage their passwords.

## Backend Setup

### Requirements
- Python 3.8+
- SQLite

### Installation
1. Navigate to the `Backend` directory:
   ```bash
   cd Backend
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend Setup

### Requirements
- Node.js
- npm

### Installation
1. Navigate to the `Frontend` directory:
   ```bash
   cd Frontend
   ```
2. Install the required npm packages:
   ```bash
   npm install
   ```
3. Run the React application:
   ```bash
   npm start
   ```

## Usage
- Access the application at `http://localhost:3000`.
- Use the application to register new users, log in, and change passwords.

## Notes
- Ensure the backend server is running before accessing the frontend application.
- The backend uses SQLite for data storage, with tables created automatically on startup.

## Contributions
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
