# Education Tutor Platform

An offline-first tutoring platform designed specifically for remote areas where internet connectivity is limited or unreliable.

## Features

### Core Functionality
- **User Management**: Registration and login for students and tutors
- **Lesson Management**: Browse and study lessons organized by subject and grade level
- **Practice Problems**: Interactive practice questions with detailed explanations
- **Quizzes**: Take quizzes with instant grading and performance analytics
- **Progress Tracking**: Monitor learning progress with completion percentages and time spent
- **Messaging System**: Direct messaging between students and tutors

### Offline-First Architecture
- **Local Storage**: All data is cached locally using browser localStorage
- **Offline Sync**: Works seamlessly without internet connection
- **Automatic Caching**: API responses are automatically cached for offline access
- **Local Database**: SQLite backend for persistent data storage

## Project Structure

```
.
├── backend/              # Python Flask API
│   ├── app/
│   │   ├── models/       # Database models
│   │   ├── routes/       # API endpoints
│   │   ├── utils/        # Helper functions
│   │   └── __init__.py   # Flask app initialization
│   ├── run.py           # Start server
│   └── requirements.txt  # Python dependencies
├── frontend/            # React web application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── utils/       # Utilities (API, auth, offline storage)
│   │   ├── styles/      # CSS stylesheets
│   │   ├── App.js       # Main app component
│   │   └── index.js     # React entry point
│   ├── public/
│   │   └── index.html   # HTML template
│   └── package.json     # Node dependencies
└── README.md           # This file
```

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **CORS**: Flask-CORS for cross-origin requests
- **ORM**: SQLAlchemy for database operations

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Icons**: React Icons
- **States**: Local state management with hooks
- **Offline Storage**: Browser localStorage API

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+ and npm
- Git

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

   The application will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `GET /api/users/all` - Get all users
- `GET /api/users/<id>` - Get user details
- `PUT /api/users/<id>` - Update user

### Lessons
- `GET /api/lessons` - Get all lessons
- `GET /api/lessons/<id>` - Get lesson details
- `POST /api/lessons` - Create lesson
- `PUT /api/lessons/<id>` - Update lesson
- `GET /api/lessons/subjects` - Get all subjects
- `GET /api/lessons/grade-levels` - Get all grade levels

### Quizzes
- `GET /api/quizzes` - Get all quizzes
- `GET /api/quizzes/<id>` - Get quiz details
- `POST /api/quizzes` - Create quiz
- `POST /api/quizzes/<id>/submit` - Submit quiz answers
- `GET /api/quizzes/attempts/<userId>` - Get user's attempts

### Progress
- `POST /api/progress` - Create/update progress
- `GET /api/progress/<userId>` - Get user progress
- `GET /api/progress/stats/<userId>` - Get learning statistics

### Messages
- `POST /api/messages` - Send message
- `GET /api/messages/inbox/<userId>` - Get inbox
- `GET /api/messages/sent/<userId>` - Get sent messages
- `GET /api/messages/conversation/<userId>/<otherUserId>` - Get conversation
- `PUT /api/messages/<id>/mark-read` - Mark message as read

## Usage

### For Students
1. Register or login with your credentials
2. Browse available lessons by subject and grade
3. Study lesson content and practice problems
4. Take quizzes to test your knowledge
5. Track your progress in the dashboard
6. Message tutors for help

### For Tutors
1. Create lessons and practice problems
2. Design quizzes with custom questions
3. Monitor student progress and performance
4. Respond to student messages
5. Provide feedback through the messaging system

## Offline Features

The platform is designed to work completely offline:
- Local data caching of all lessons, quizzes, and user progress
- Offline quiz attempts are saved locally
- Messages can be composed offline and sent when connection is available
- Automatic syncing when connection is restored

## Database Schema

### Main Tables
- **users**: User account information
- **lessons**: Course lessons and content
- **practice_problems**: Practice questions for lessons
- **quizzes**: Quiz definitions and metadata
- **quiz_questions**: Individual quiz questions
- **quiz_attempts**: Student quiz submissions
- **student_answers**: Individual student answers
- **progress**: Student learning progress tracking
- **messages**: Direct messages between users

## Configuration

### API Base URL
Update in `frontend/src/utils/apiService.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Database Path
Update in `backend/app/__init__.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/tutoring.db'
```

## Running the Application

### Start Backend
```bash
cd backend
python run.py
```

### Start Frontend
```bash
cd frontend
npm start
```

Both should be running simultaneously for full functionality.

## Features for Remote Areas

1. **Minimal Data Usage**: Efficient API calls with caching
2. **Offline-First Design**: App functions fully without internet
3. **Local Data Storage**: SQLite doesn't require internet
4. **Flexible Sync**: Data syncs when connection available
5. **Progressive Enhancement**: Works on slow connections
6. **Lightweight Assets**: Optimized for low bandwidth

## Future Enhancements

- [ ] Mobile app using React Native
- [ ] Advanced analytics and reporting
- [ ] Video content support (local encoding)
- [ ] Peer-to-peer sync for offline networks
- [ ] Accessibility improvements
- [ ] Multi-language support
- [ ] Audio content for low-bandwidth areas
- [ ] Push notifications
- [ ] Gamification features
- [ ] Real-time collaboration tools

## Troubleshooting

### Port Already in Use
- Backend port 5000: `python run.py --port 5001`
- Frontend port 3000: `PORT=3001 npm start`

### Database Errors
- Delete `instance/tutoring.db` to reset database
- Database recreates automatically on next run

### CORS Issues
- Ensure Flask-CORS is installed: `pip install Flask-CORS`
- Check API_BASE_URL in frontend matches backend URL

### Offline Storage Not Working
- Check browser localStorage is enabled
- Clear localStorage if corrupted: `localStorage.clear()`

## License

MIT License - Feel free to use and modify

## Support

For issues and questions, please create an issue in the repository.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.
