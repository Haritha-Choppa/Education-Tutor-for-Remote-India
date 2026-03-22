from flask import Blueprint, request, jsonify
from app import db
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt, StudentAnswer
from datetime import datetime

bp = Blueprint('quizzes', __name__, url_prefix='/api/quizzes')

@bp.route('', methods=['GET'])
def get_quizzes():
    """Get all quizzes"""
    lesson_id = request.args.get('lesson_id')
    
    query = Quiz.query
    if lesson_id:
        query = query.filter_by(lesson_id=lesson_id)
    
    quizzes = query.all()
    return jsonify([q.to_dict() for q in quizzes]), 200

@bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get quiz with all questions"""
    quiz = Quiz.query.get(quiz_id)
    
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    quiz_data = quiz.to_dict()
    quiz_data['questions'] = [q.to_dict() for q in quiz.questions]
    
    return jsonify(quiz_data), 200

@bp.route('', methods=['POST'])
def create_quiz():
    """Create a new quiz"""
    data = request.get_json()
    
    if not data or not data.get('lesson_id') or not data.get('title'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    quiz = Quiz(
        lesson_id=data['lesson_id'],
        title=data['title'],
        description=data.get('description', ''),
        total_questions=data.get('total_questions', 0),
        passing_score=data.get('passing_score', 70.0),
        time_limit=data.get('time_limit')
    )
    
    db.session.add(quiz)
    db.session.commit()
    
    return jsonify(quiz.to_dict()), 201

@bp.route('/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    """Submit quiz answers and calculate score"""
    data = request.get_json(silent=True) or {}
    
    if not data or not data.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Create attempt record first so child answers can reference a valid attempt_id.
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=data['user_id']
    )

    db.session.add(attempt)
    db.session.flush()

    total_points = 0
    earned_points = 0
    answers = data.get('answers', [])

    try:
        # Process each answer
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            if question_id is None:
                continue

            question = QuizQuestion.query.filter_by(id=question_id, quiz_id=quiz_id).first()
            if not question:
                continue

            total_points += question.points
            provided_answer = str(answer_data.get('answer', '')).strip()
            is_correct = provided_answer.lower() == str(question.correct_answer).strip().lower()

            if is_correct:
                earned_points += question.points

            student_answer = StudentAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                student_answer=provided_answer,
                is_correct=is_correct,
                points_earned=question.points if is_correct else 0
            )
            db.session.add(student_answer)

        # Calculate final score
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        attempt.score = earned_points
        attempt.percentage = percentage
        attempt.passed = percentage >= quiz.passing_score
        attempt.completed_at = datetime.utcnow()

        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Unable to submit quiz. Please try again.'}), 500
    
    return jsonify({
        'attempt_id': attempt.id,
        'score': attempt.score,
        'percentage': attempt.percentage,
        'passed': attempt.passed,
        'passing_score': quiz.passing_score
    }), 200

@bp.route('/attempts/<int:user_id>', methods=['GET'])
def get_user_quiz_attempts(user_id):
    """Get all quiz attempts for a user"""
    attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in attempts]), 200

@bp.route('/attempt/<int:attempt_id>', methods=['GET'])
def get_attempt_details(attempt_id):
    """Get detailed attempt results"""
    attempt = QuizAttempt.query.get(attempt_id)
    
    if not attempt:
        return jsonify({'error': 'Attempt not found'}), 404
    
    attempt_data = attempt.to_dict()
    attempt_data['answers'] = [a.to_dict() for a in attempt.student_answers]
    
    return jsonify(attempt_data), 200
