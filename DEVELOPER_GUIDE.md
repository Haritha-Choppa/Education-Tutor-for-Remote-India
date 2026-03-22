# Education Tutor Platform - Developer Guide

## Architecture Overview

The Education Tutor Platform is built with a client-server architecture optimized for offline operation in remote areas.

### System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     User Devices                              │
│  (Laptops, Tablets, Computers - with browsers)                │
└────────────────────────────┬─────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   React App     │
                    │  Port 3000      │
                    │  (Browser)      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
    Local Storage       HTTP API            IndexedDB
    (Offline Data)   (Syncs when online)  (Future use)
        │                    │                    │
        │                    ▼                    │
        │        ┌─────────────────────┐          │
        │        │  Flask API Server   │          │
        │        │  Port 5000          │          │
        │        │  (Python/Flask)     │          │
        │        └────────┬────────────┘          │
        │                 │                       │
        │                 ▼                       │
        │        ┌─────────────────────┐          │
        └──────▶ │  SQLite Database    │          │
                 │  (tutoring.db)      │          │
                 │  Local Storage      │          │
                 └─────────────────────┘          │
        ┌────────────────────────────────────────┘
        │
        ▼ (Optional - Future Cloud Sync)
    ☁️ Cloud Storage (PostgreSQL/MongoDB)
```

### Data Flow

1. **Online Mode**:
   - Frontend makes API calls to backend
   - Responses cached to localStorage
   - State synced with server

2. **Offline Mode**:
   - All data served from localStorage
   - Local changes queued
   - Automatic sync on reconnection

3. **Hybrid Mode**:
   - Tries API first
   - Falls back to cache on failure
   - Seamless for users

## Component Structure

### Backend Components

```
backend/
├── app/
│   ├── models/
│   │   ├── user.py              # User entity
│   │   ├── lesson.py            # Lessons and practice
│   │   ├── quiz.py              # Quizzes and attempts
│   │   ├── message.py           # Messaging system
│   │   ├── progress.py          # Learning progress
│   │   └── conversation.py      # Chat conversations
│   │
│   ├── routes/
│   │   ├── users.py             # Auth endpoints
│   │   ├── lessons.py           # Lesson endpoints
│   │   ├── quizzes.py           # Quiz endpoints
│   │   ├── messages.py          # Messaging endpoints
│   │   └── progress.py          # Analytics endpoints
│   │
│   ├── utils/
│   │   └── __init__.py          # Helper functions
│   │
│   └── __init__.py              # App factory
│
├── run.py                        # Entry point
├── init_db.py                    # Database initialization
└── requirements.txt              # Python dependencies
```

### Frontend Components

```
frontend/src/
├── components/
│   ├── Login.js                 # Login page
│   ├── Register.js              # Registration page
│   ├── Dashboard.js             # Student dashboard
│   ├── LessonsList.js           # Lessons browser
│   ├── LessonDetail.js          # Lesson viewer
│   ├── QuizzesList.js           # Quiz browser
│   ├── QuizAttempt.js           # Quiz taker
│   └── Messages.js              # Chat interface
│
├── utils/
│   ├── authContext.js           # Auth state management
│   ├── apiService.js            # API client (with caching)
│   └── offlineStorage.js        # LocalStorage manager
│
├── styles/
│   ├── global.css               # Overall styles
│   ├── auth.css                 # Auth pages
│   ├── lessons.css              # Lessons page
│   ├── lesson-detail.css        # Lesson detail
│   ├── dashboard.css            # Dashboard
│   ├── quiz.css                 # Quiz page
│   ├── quizzes.css              # Quizzes list
│   └── messages.css             # Messages
│
├── App.js                       # Main app component
└── index.js                     # React entry point
```

## Database Schema

### Users Table
```sql
users
├── id (PK)
├── username (unique)
├── email (unique)
├── password_hash
├── full_name
├── role (student/tutor/admin)
├── grade_level
├── created_at
└── updated_at
```

### Lessons Table
```sql
lessons
├── id (PK)
├── title
├── description
├── subject
├── grade_level
├── content (markdown/HTML)
├── video_url (path or base64)
├── order
├── created_at
└── updated_at
```

### Practice Problems Table
```sql
practice_problems
├── id (PK)
├── lesson_id (FK)
├── question
├── question_type (multiple_choice/essay/numeric)
├── options (JSON)
├── correct_answer
├── explanation
├── difficulty (easy/medium/hard)
└── created_at
```

### Quizzes Table
```sql
quizzes
├── id (PK)
├── lesson_id (FK)
├── title
├── description
├── total_questions
├── passing_score (%)
├── time_limit (minutes)
└── created_at
```

### Quiz Responses Table
```sql
quiz_attempts
├── id (PK)
├── quiz_id (FK)
├── user_id (FK)
├── score (points)
├── percentage (%)
├── passed (boolean)
├── started_at
└── completed_at
```

### Progress Table
```sql
progress
├── id (PK)
├── user_id (FK)
├── lesson_id (FK)
├── completion_percentage (0-100)
├── time_spent (seconds)
├── is_completed (boolean)
├── started_at
└── completed_at
```

### Messages Table
```sql
messages
├── id (PK)
├── sender_id (FK to users)
├── receiver_id (FK to users)
├── subject
├── message_body
├── is_read (boolean)
├── created_at
└── read_at
```

## API Reference

### Authentication Routes

#### POST /api/users/register
Register a new user account
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "role": "student",
  "grade_level": "Grade 10"
}
```

#### POST /api/users/login
Login user
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

### Lesson Routes

#### GET /api/lessons?subject=Math&grade_level=Grade%2010
Get filtered lessons

#### GET /api/lessons/{id}
Get specific lesson with practice problems

#### POST /api/lessons
Create new lesson

### Quiz Routes

#### GET /api/quizzes?lesson_id=1
Get quizzes for a lesson

#### GET /api/quizzes/{id}
Get quiz details with questions

#### POST /api/quizzes/{id}/submit
Submit quiz answers
```json
{
  "user_id": 1,
  "answers": [
    {"question_id": 1, "answer": "Option A"},
    {"question_id": 2, "answer": "4"}
  ]
}
```

### Progress Routes

#### POST /api/progress
Update progress
```json
{
  "user_id": 1,
  "lesson_id": 5,
  "completion_percentage": 75,
  "is_completed": false,
  "time_spent": 3600
}
```

#### GET /api/progress/stats/{userId}
Get user statistics
```json
{
  "total_lessons": 10,
  "completed_lessons": 3,
  "total_time_spent": 7200,
  "average_completion": 45.5,
  "completion_rate": 30.0
}
```

### Message Routes

#### POST /api/messages
Send message
```json
{
  "sender_id": 1,
  "receiver_id": 2,
  "subject": "Help with Algebra",
  "message_body": "I need help with Problem 5..."
}
```

#### GET /api/messages/inbox/{userId}
Get inbox messages

#### GET /api/messages/conversation/{userId}/{otherUserId}
Get conversation between users

## Offline Functionality

### How It Works

1. **API Caching**:
   ```javascript
   // In apiService.js
   const withOfflineSupport = async (apiCall, storageKey) => {
     try {
       const response = await apiCall();
       localStorage.setItem(storageKey, JSON.stringify(response.data));
       return response.data;
     } catch {
       return JSON.parse(localStorage.getItem(storageKey));
     }
   };
   ```

2. **Local Storage Structure**:
   ```javascript
   localStorage.setItem('lessons', JSON.stringify(lessons));
   localStorage.setItem('quizzes', JSON.stringify(quizzes));
   localStorage.setItem('progress', JSON.stringify(progress));
   localStorage.setItem('messages', JSON.stringify(messages));
   localStorage.setItem('currentUser', JSON.stringify(user));
   ```

3. **Graceful Degradation**:
   - Online: Real-time syncing
   - Offline: Cached data used
   - Reconnect: Automatic sync

### Local Storage Limits
- Chrome: ~10MB per app
- Firefox: ~10MB per app
- Storage for lessons/quizzes can be managed with pagination

## Adding Sample Data

### Automated Way

Run the initialization script:
```bash
cd backend
python init_db.py
```

This creates:
- 2 sample lessons (Algebra, Photosynthesis)
- 2 quizzes with 3 questions each
- Practice problems

### Manual Way

```python
from app import create_app, db
from app.models.lesson import Lesson
from app.models.quiz import Quiz, QuizQuestion

app = create_app()

with app.app_context():
    # Create lesson
    lesson = Lesson(
        title="New Topic",
        description="Learn new things",
        subject="Math",
        grade_level="Grade 9",
        content="Content here...",
        order=1
    )
    db.session.add(lesson)
    db.session.commit()
    
    # Create quiz
    quiz = Quiz(
        lesson_id=lesson.id,
        title="Quiz 1",
        description="Test your knowledge",
        total_questions=5,
        passing_score=70.0
    )
    db.session.add(quiz)
    db.session.commit()
```

## Customization Guide

### Changing Colors

Edit `frontend/src/styles/global.css`:
```css
:root {
  --primary-color: #4CAF50;    /* Green */
  --secondary-color: #2196F3;  /* Blue */
  --danger-color: #f44336;     /* Red */
}
```

### Adding New Subject

1. Create lessons with new subject in database
2. Lessons appear automatically in subject filter

### Custom Branding

Edit `frontend/public/index.html`:
```html
<title>Your School Name - Education Platform</title>
```

Edit components headers:
```javascript
// In components
<h1>Your School Name</h1>
```

## Deployment

### Local Network
```bash
# Backend: Allow all interfaces
python run.py --host 0.0.0.0

# Access from other computers
http://<your-ip>:5000

# Update frontend
const API_BASE_URL = 'http://<your-ip>:5000/api';
```

### Docker (Future)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

## Performance Tips

1. **Database Indexing**: Add indexes on frequently queried fields
2. **Pagination**: Implement pagination for large lesson lists
3. **Caching Strategy**: Cache lessons for a week, quizzes for a day
4. **Image Optimization**: Compress images in lessons
5. **Code Splitting**: Lazy load React components

## Security Considerations

1. **Password**: Hash with werkzeug.security
2. **CORS**: Limit to known origins in production
3. **SQL Injection**: Using SQLAlchemy ORM prevents this
4. **XSS**: React automatically escapes content
5. **HTTPS**: Use in production deployment

## Testing

### Backend Testing
```bash
# Install pytest
pip install pytest pytest-flask

# Run tests
pytest backend/
```

### Frontend Testing
```bash
# Run tests
npm test
```

## Monitoring & Debugging

### Check Backend Logs
```
[2024-01-15 10:30:15] INFO: Started server
[2024-01-15 10:30:20] INFO: Login request from user: john_doe
```

### Check Browser Console
```javascript
// Open DevTools (F12)
// See API calls in Network tab
// Check errors in Console
```

## Future Features

1. **Video Streaming**: Embed videos in lessons
2. **Audio Content**: For low-bandwidth areas
3. **Sync Server**: Cloud backup
4. **Mobile App**: React Native version
5. **Widgets**: Integration with learning management systems
6. **Analytics**: Advanced reporting
7. **Gamification**: Badges and achievements
8. **Collaboration**: Group projects

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Change port or kill process |
| CORS errors | Check API_BASE_URL in frontend |
| Database locked | Delete DB and reinitialize |
| Offline not working | Check localStorage enabled |
| Slow performance | Clear localStorage and cache |

## References

- Flask: https://flask.palletsprojects.com/
- React: https://react.dev/
- SQLAlchemy: https://www.sqlalchemy.org/
- Axios: https://axios-http.com/

---

**Last Updated**: 2024
**Version**: 1.0
**License**: MIT
