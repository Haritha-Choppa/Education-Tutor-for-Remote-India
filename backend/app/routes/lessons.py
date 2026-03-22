from flask import Blueprint, request, jsonify
from app import db
from app.models.lesson import Lesson, PracticeProblem

bp = Blueprint('lessons', __name__, url_prefix='/api/lessons')

@bp.route('', methods=['GET'])
def get_lessons():
    """Get all lessons with optional filters"""
    subject = request.args.get('subject')
    grade_level = request.args.get('grade_level')
    
    query = Lesson.query
    if subject:
        query = query.filter_by(subject=subject)
    if grade_level:
        query = query.filter_by(grade_level=grade_level)
    
    lessons = query.order_by(Lesson.order).all()
    return jsonify([lesson.to_dict() for lesson in lessons]), 200

@bp.route('/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get a specific lesson with its practice problems"""
    lesson = Lesson.query.get(lesson_id)
    
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    lesson_data = lesson.to_dict()
    lesson_data['practice_problems'] = [p.to_dict() for p in lesson.practice_problems]
    
    return jsonify(lesson_data), 200

@bp.route('', methods=['POST'])
def create_lesson():
    """Create a new lesson"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('subject'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    lesson = Lesson(
        title=data['title'],
        description=data.get('description', ''),
        subject=data['subject'],
        grade_level=data.get('grade_level', ''),
        content=data.get('content', ''),
        video_url=data.get('video_url', ''),
        order=data.get('order', 0)
    )
    
    db.session.add(lesson)
    db.session.commit()
    
    return jsonify(lesson.to_dict()), 201

@bp.route('/<int:lesson_id>', methods=['PUT'])
def update_lesson(lesson_id):
    """Update a lesson"""
    lesson = Lesson.query.get(lesson_id)
    
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        lesson.title = data['title']
    if 'description' in data:
        lesson.description = data['description']
    if 'content' in data:
        lesson.content = data['content']
    if 'video_url' in data:
        lesson.video_url = data['video_url']
    if 'order' in data:
        lesson.order = data['order']
    
    db.session.commit()
    
    return jsonify(lesson.to_dict()), 200

@bp.route('/<int:lesson_id>/practice-problems', methods=['GET'])
def get_practice_problems(lesson_id):
    """Get practice problems for a lesson"""
    lesson = Lesson.query.get(lesson_id)
    
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    problems = PracticeProblem.query.filter_by(lesson_id=lesson_id).all()
    return jsonify([p.to_dict() for p in problems]), 200

@bp.route('/practice-problems', methods=['POST'])
def create_practice_problem():
    """Create a practice problem"""
    data = request.get_json()
    
    if not data or not data.get('lesson_id') or not data.get('question'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    problem = PracticeProblem(
        lesson_id=data['lesson_id'],
        question=data['question'],
        question_type=data.get('question_type', 'multiple_choice'),
        options=data.get('options'),
        correct_answer=data['correct_answer'],
        explanation=data.get('explanation', ''),
        difficulty=data.get('difficulty', 'medium')
    )
    
    db.session.add(problem)
    db.session.commit()
    
    return jsonify(problem.to_dict()), 201

@bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all unique subjects"""
    subjects = db.session.query(Lesson.subject).distinct().all()
    return jsonify([s[0] for s in subjects]), 200

@bp.route('/grade-levels', methods=['GET'])
def get_grade_levels():
    """Get all grade levels"""
    grades = db.session.query(Lesson.grade_level).distinct().all()
    return jsonify([g[0] for g in grades]), 200
