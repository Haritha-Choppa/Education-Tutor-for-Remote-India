# INTEL 3 - Education Tutor Platform Setup Guide

## Quick Start

This folder contains a complete offline-first education tutoring platform for remote areas.

### Folder Structure
```
├── backend/              Python Flask API with SQLite database
├── frontend/            React web application
└── README.md            Detailed documentation
```

## Prerequisites
- Python 3.8+
- Node.js 14+ & npm
- A modern web browser

## Setup Instructions

### 1. Backend Setup

#### Windows:
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize sample data
python init_db.py

# Run server
python run.py
```

#### macOS/Linux:
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize sample data
python init_db.py

# Run server
python run.py
```

The API will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The application will open on `http://localhost:3000`

## Features

### ✅ Fully Offline-Capable
- All data cached locally using browser localStorage
- App works without internet connection
- Automatic syncing when connection available

### ✅ Complete Learning Platform
- View lessons by subject and grade level
- Interactive practice problems
- Quizzes with instant grading
- Track learning progress
- Direct messaging system

### ✅ User Management
- Student and tutor roles
- User profiles and authentication
- Learning statistics and analytics

## Sample Credentials

**Test these accounts after running `init_db.py`:**

The database will be populated with sample content:
- Grade 8 Mathematics: Introduction to Algebra
- Grade 9 Biology: Photosynthesis
- 3 quizzes with multiple questions
- Practice problems

## Key Endpoints

```
Backend API: http://localhost:5000
Frontend App: http://localhost:3000

Sample API calls:
- Login: POST /api/users/login
- Get Lessons: GET /api/lessons
- Get Quizzes: GET /api/quizzes
- Submit Quiz: POST /api/quizzes/1/submit
- Send Message: POST /api/messages
```

## Important Files

### Backend
- `backend/run.py` - Start Flask server
- `backend/app/__init__.py` - App configuration
- `backend/app/models/` - Database models
- `backend/app/routes/` - API endpoints
- `backend/init_db.py` - Initialize with sample data

### Frontend
- `frontend/src/App.js` - Main app component
- `frontend/src/utils/apiService.js` - API client with offline support
- `frontend/src/utils/offlineStorage.js` - Local storage manager
- `frontend/src/components/` - React components

## Offline Features

The platform is designed for remote areas with limited connectivity:

1. **Data Caching**: All API responses cached to localStorage
2. **Offline-First Design**: App fully functional without internet
3. **Automatic Sync**: Data persists and syncs when connection restored
4. **Database**: SQLite for persistent backend storage

## Troubleshooting

### Port Already in Use
- Backend: `python run.py --port 5001`
- Frontend: `PORT=3001 npm start`

### Module Not Found (Python)
```bash
cd backend
pip install -r requirements.txt
```

### npm packages missing
```bash
cd frontend
npm install
```

### Database errors
Delete `backend/instance/tutoring.db` and run `python init_db.py` again

## Development Workflow

1. **Terminal 1**: Start backend
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python run.py
   ```

2. **Terminal 2**: Start frontend
   ```bash
   cd frontend
   npm start
   ```

3. **Browser**: Open http://localhost:3000

## Testing

### Test Student Flow
1. Register or use existing student account
2. Browse lessons in the Lessons tab
3. Take a quiz in the Quizzes tab
4. Check progress in Dashboard
5. Send a message to a tutor

### Test Offline
1. Open browser DevTools (F12)
2. Go to Network tab
3. Check "Offline" checkbox
4. App continues to work with cached data

## Next Steps

1. Review the main [README.md](./README.md) for detailed documentation
2. Explore the code structure
3. Add your own lessons and quizzes
4. Customize the UI in `frontend/src/styles/`
5. Extend features as needed

## Support

For detailed documentation, see [README.md](./README.md)

For issues, check:
- Backend logs in terminal
- Browser console (F12 > Console)
- Network requests (F12 > Network)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  React App (Port 3000)                           │  │
│  │  - Login/Register                                │  │
│  │  - Dashboard                                      │  │
│  │  - Lessons & Quizzes                            │  │
│  │  - Messages                                       │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                   │                      │
│         HTTP API            localStorage                │
│       (Cached)             (Offline Data)               │
│               │                   │                      │
└───────────────┼───────────────────┼──────────────────────┘
                │                   │
  ┌─────────────▼─────────────┐     │
  │  Flask API (Port 5000)    │     │
  │  - User Management        │     │
  │  - Lessons/Quizzes        │     │
  │  - Messages               │     │
  │  - Progress Tracking      │     ▼
  ├─────────────┬─────────────┤  Browser
  │   SQLite    │   CORS      │  LocalStorage
  │  Database   │  Handler    │
  └─────────────┴─────────────┘
```

Happy Learning! 🎓
