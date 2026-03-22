from app import db
from datetime import datetime

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text)  # Can store markdown or HTML
    video_url = db.Column(db.String(500))  # Local file path or base64 encoded video
    order = db.Column(db.Integer)  # Order within course
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    practice_problems = db.relationship('PracticeProblem', backref='lesson', lazy=True, cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='lesson', lazy=True, cascade='all, delete-orphan')
    progress_records = db.relationship('Progress', backref='lesson', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'grade_level': self.grade_level,
            'content': self.content,
            'video_url': self.video_url,
            'order': self.order,
            'created_at': self.created_at.isoformat()
        }

class PracticeProblem(db.Model):
    __tablename__ = 'practice_problems'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50))  # multiple_choice, essay, numeric, etc.
    options = db.Column(db.JSON)  # For multiple choice
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'question': self.question,
            'question_type': self.question_type,
            'options': self.options,
            'explanation': self.explanation,
            'difficulty': self.difficulty
        }
