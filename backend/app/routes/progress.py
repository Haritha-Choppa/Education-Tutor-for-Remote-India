from flask import Blueprint, request, jsonify
from app import db
from app.models.progress import Progress
from datetime import datetime

bp = Blueprint('progress', __name__, url_prefix='/api/progress')

@bp.route('', methods=['POST'])
def create_progress():
    """Create or update progress record"""
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('lesson_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if progress record exists
    progress = Progress.query.filter_by(
        user_id=data['user_id'],
        lesson_id=data['lesson_id']
    ).first()
    
    if progress:
        progress.completion_percentage = data.get('completion_percentage', progress.completion_percentage)
        progress.time_spent = data.get('time_spent', progress.time_spent)
        progress.is_completed = data.get('is_completed', progress.is_completed)
        
        if progress.is_completed and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
    else:
        progress = Progress(
            user_id=data['user_id'],
            lesson_id=data['lesson_id'],
            completion_percentage=data.get('completion_percentage', 0),
            time_spent=data.get('time_spent', 0),
            is_completed=data.get('is_completed', False)
        )
        
        if progress.is_completed:
            progress.completed_at = datetime.utcnow()
        
        db.session.add(progress)
    
    db.session.commit()
    
    return jsonify(progress.to_dict()), 200 if not data.get('completion_percentage') else 201

@bp.route('/<int:user_id>', methods=['GET'])
def get_user_progress(user_id):
    """Get all progress records for a user"""
    progress_records = Progress.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in progress_records]), 200

@bp.route('/lesson/<int:lesson_id>', methods=['GET'])
def get_lesson_progress(lesson_id):
    """Get all progress for a lesson (for tutors)"""
    progress_records = Progress.query.filter_by(lesson_id=lesson_id).all()
    return jsonify([p.to_dict() for p in progress_records]), 200

@bp.route('/<int:user_id>/<int:lesson_id>', methods=['GET'])
def get_lesson_user_progress(user_id, lesson_id):
    """Get progress for a specific user and lesson"""
    progress = Progress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        return jsonify({'error': 'Progress not found'}), 404
    
    return jsonify(progress.to_dict()), 200

@bp.route('/stats/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    """Get learning statistics for a user"""
    progress_records = Progress.query.filter_by(user_id=user_id).all()
    
    total_lessons = len(progress_records)
    completed_lessons = sum(1 for p in progress_records if p.is_completed)
    total_time = sum(p.time_spent for p in progress_records)
    avg_completion = sum(p.completion_percentage for p in progress_records) / total_lessons if total_lessons > 0 else 0
    
    return jsonify({
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'total_time_spent': total_time,
        'average_completion': avg_completion,
        'completion_rate': (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    }), 200
