from flask import Blueprint, request, jsonify
from app import db
from app.models.message import Message
from datetime import datetime

bp = Blueprint('messages', __name__, url_prefix='/api/messages')

@bp.route('', methods=['POST'])
def send_message():
    """Send a message"""
    data = request.get_json()
    
    if not data or not data.get('sender_id') or not data.get('receiver_id') or not data.get('message_body'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    message = Message(
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        subject=data.get('subject', ''),
        message_body=data['message_body']
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify(message.to_dict()), 201

@bp.route('/inbox/<int:user_id>', methods=['GET'])
def get_inbox(user_id):
    """Get all messages for a user (received)"""
    messages = Message.query.filter_by(receiver_id=user_id).order_by(Message.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@bp.route('/sent/<int:user_id>', methods=['GET'])
def get_sent_messages(user_id):
    """Get all sent messages from a user"""
    messages = Message.query.filter_by(sender_id=user_id).order_by(Message.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    """Get a specific message"""
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    # Mark as read
    if not message.is_read:
        message.is_read = True
        message.read_at = datetime.utcnow()
        db.session.commit()
    
    return jsonify(message.to_dict()), 200

@bp.route('/<int:message_id>/mark-read', methods=['PUT'])
def mark_read(message_id):
    """Mark message as read"""
    message = Message.query.get(message_id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    message.is_read = True
    message.read_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(message.to_dict()), 200

@bp.route('/conversation/<int:user_id>/<int:other_user_id>', methods=['GET'])
def get_conversation(user_id, other_user_id):
    """Get conversation between two users"""
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == user_id, Message.receiver_id == other_user_id),
            db.and_(Message.sender_id == other_user_id, Message.receiver_id == user_id)
        )
    ).order_by(Message.created_at).all()
    
    return jsonify([m.to_dict() for m in messages]), 200

@bp.route('/unread-count/<int:user_id>', methods=['GET'])
def get_unread_count(user_id):
    """Get count of unread messages"""
    count = Message.query.filter_by(receiver_id=user_id, is_read=False).count()
    return jsonify({'unread_count': count}), 200
