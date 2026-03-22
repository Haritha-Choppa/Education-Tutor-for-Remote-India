from app import db

class ChatConversation(db.Model):
    """Model for storing chat conversations"""
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    last_message_at = db.Column(db.DateTime)
    
    # For future reference to get unread count
    def get_unread_count(self, user_id):
        from app.models.message import Message
        return Message.query.filter(
            Message.receiver_id == user_id,
            Message.is_read == False,
            db.or_(
                db.and_(Message.sender_id == self.user1_id, Message.receiver_id == user_id),
                db.and_(Message.sender_id == self.user2_id, Message.receiver_id == user_id)
            )
        ).count()
