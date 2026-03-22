from flask import Blueprint, request, jsonify
from flask import current_app
from app import db
from app.models.user import User
from app.models.password_reset_token import PasswordResetToken
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from email.message import EmailMessage
import hashlib
import re
import secrets
import smtplib

bp = Blueprint('users', __name__, url_prefix='/api/users')


PASSWORD_SPECIAL_CHARS = r"[^A-Za-z0-9]"


def validate_password_strength(password):
    """Enforce strong password policy."""
    if not isinstance(password, str):
        return "Password is required"

    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return "Password must include at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must include at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return "Password must include at least one number"
    if not re.search(PASSWORD_SPECIAL_CHARS, password):
        return "Password must include at least one special character"
    return None


def _hash_token(raw_token):
    return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()


def _send_password_reset_email(to_email, reset_link):
    mail_server = current_app.config.get('MAIL_SERVER', '')
    mail_port = current_app.config.get('MAIL_PORT', 587)
    mail_use_tls = current_app.config.get('MAIL_USE_TLS', True)
    mail_username = current_app.config.get('MAIL_USERNAME', '')
    mail_password = current_app.config.get('MAIL_PASSWORD', '')
    mail_from = current_app.config.get('MAIL_FROM', mail_username)

    message = EmailMessage()
    message['Subject'] = 'TutorFlow Password Reset'
    message['From'] = mail_from
    message['To'] = to_email
    message.set_content(
        "You requested a password reset for your TutorFlow account.\n\n"
        f"Reset your password using this link (valid for a limited time):\n{reset_link}\n\n"
        "If you did not request this, please ignore this email."
    )

    if not (mail_server and mail_username and mail_password and mail_from):
        # Development fallback when SMTP is not configured.
        print(f"[Password Reset] SMTP not configured. Reset link for {to_email}: {reset_link}")
        return False

    with smtplib.SMTP(mail_server, mail_port, timeout=10) as smtp:
        if mail_use_tls:
            smtp.starttls()
        smtp.login(mail_username, mail_password)
        smtp.send_message(message)

    return True

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    password_error = validate_password_strength(data['password'])
    if password_error:
        return jsonify({'error': password_error}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        full_name=data.get('full_name', ''),
        role=data.get('role', 'student'),
        grade_level=data.get('grade_level', '')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login user (returns user data for offline storage)"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return jsonify(user.to_dict()), 200

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'grade_level' in data:
        user.grade_level = data['grade_level']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200

@bp.route('/all', methods=['GET'])
def get_all_users():
    """Get all users (tutors for messaging)"""
    role = request.args.get('role')
    
    query = User.query
    if role:
        query = query.filter_by(role=role)
    
    users = query.all()
    return jsonify([user.to_dict() for user in users]), 200


@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Generate one-time reset link and send to registered email."""
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()

    # Always return a generic response to reduce user enumeration risk.
    generic_response = {
        'message': 'If the email is registered, a password reset link has been sent.'
    }

    if not user:
        return jsonify(generic_response), 200

    now = datetime.utcnow()
    # Invalidate previous unused reset tokens for this user.
    existing_tokens = PasswordResetToken.query.filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used_at.is_(None)
    ).all()
    for token_record in existing_tokens:
        token_record.used_at = now

    raw_token = secrets.token_urlsafe(48)
    token_hash = _hash_token(raw_token)
    expires_minutes = current_app.config.get('PASSWORD_RESET_TOKEN_EXPIRY_MINUTES', 30)

    reset_token = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=now + timedelta(minutes=expires_minutes)
    )
    db.session.add(reset_token)
    db.session.commit()

    frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
    reset_link = f"{frontend_url}/reset-password?token={raw_token}"
    try:
        _send_password_reset_email(user.email, reset_link)
    except Exception:
        # Keep generic response even on mail failure to avoid leaking internals.
        pass

    return jsonify(generic_response), 200


@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using one-time token."""
    data = request.get_json(silent=True) or {}
    raw_token = (data.get('token') or '').strip()
    new_password = data.get('password') or ''

    if not raw_token or not new_password:
        return jsonify({'error': 'Token and password are required'}), 400

    confirm_password = data.get('confirm_password')
    if confirm_password is not None and new_password != confirm_password:
        return jsonify({'error': 'Password confirmation does not match'}), 400

    password_error = validate_password_strength(new_password)
    if password_error:
        return jsonify({'error': password_error}), 400

    token_hash = _hash_token(raw_token)
    token_record = PasswordResetToken.query.filter_by(token_hash=token_hash).first()

    if not token_record or token_record.is_used or token_record.is_expired:
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    user = User.query.get(token_record.user_id)
    if not user:
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    now = datetime.utcnow()
    user.password_hash = generate_password_hash(new_password)
    token_record.used_at = now

    # Invalidate any other active tokens for this user to enforce one-time reset flow.
    other_tokens = PasswordResetToken.query.filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.id != token_record.id,
        PasswordResetToken.used_at.is_(None)
    ).all()
    for other in other_tokens:
        other.used_at = now

    db.session.commit()

    return jsonify({'message': 'Password reset successful. Please login with your new password.'}), 200
