import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../utils/authContext';
import { apiService } from '../utils/apiService';
import '../styles/messages.css';

const Messages = () => {
  const { user } = useAuth();
  const [inbox, setInbox] = useState([]);
  const [sent, setSent] = useState([]);
  const [users, setUsers] = useState([]);
  const [activeTab, setActiveTab] = useState('inbox');
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [subject, setSubject] = useState('');
  const [loading, setLoading] = useState(true);

  const loadMessagesData = useCallback(async () => {
    if (!user) return;

    try {
      setLoading(true);
      const [inboxData, sentData, usersData] = await Promise.all([
        apiService.getInbox(user.id),
        apiService.getSentMessages(user.id),
        apiService.getAllUsers()
      ]);
      
      setInbox(inboxData || []);
      setSent(sentData || []);
      setUsers((usersData || []).filter(u => u.id !== user.id)); // Exclude current user
    } catch (error) {
      console.error('Error loading messages:', error);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    loadMessagesData();
  }, [loadMessagesData]);

  const handleOpenConversation = async (otherUserId) => {
    try {
      const conversationData = await apiService.getConversation(user.id, otherUserId);
      setConversation(conversationData || []);
      setSelectedConversation(otherUserId);
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!messageText.trim() || !selectedConversation) return;

    try {
      const newMessage = await apiService.sendMessage({
        sender_id: user.id,
        receiver_id: selectedConversation,
        subject: subject || 'No Subject',
        message_body: messageText
      });

      setConversation([...conversation, newMessage]);
      setMessageText('');
      setSubject('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading messages...</div>;
  }

  return (
    <div className="messages-container">
      <h1>Messages</h1>
      
      <div className="messages-layout">
        <div className="messages-sidebar">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'inbox' ? 'active' : ''}`}
              onClick={() => setActiveTab('inbox')}
            >
              Inbox ({inbox.length})
            </button>
            <button
              className={`tab ${activeTab === 'sent' ? 'active' : ''}`}
              onClick={() => setActiveTab('sent')}
            >
              Sent ({sent.length})
            </button>
            <button
              className={`tab ${activeTab === 'compose' ? 'active' : ''}`}
              onClick={() => setActiveTab('compose')}
            >
              New Message
            </button>
          </div>

          {activeTab === 'inbox' && (
            <div className="messages-list">
              {inbox.length === 0 ? (
                <p className="empty">No messages</p>
              ) : (
                inbox.map(msg => (
                  <div
                    key={msg.id}
                    className={`message-item ${!msg.is_read ? 'unread' : ''}`}
                    onClick={() => handleOpenConversation(msg.sender_id)}
                  >
                    <h4>{msg.sender_name}</h4>
                    <p className="subject">{msg.subject}</p>
                    <p className="time">{new Date(msg.created_at).toLocaleDateString()}</p>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'sent' && (
            <div className="messages-list">
              {sent.length === 0 ? (
                <p className="empty">No sent messages</p>
              ) : (
                sent.map(msg => (
                  <div
                    key={msg.id}
                    className="message-item"
                    onClick={() => handleOpenConversation(msg.receiver_id)}
                  >
                    <h4>To: {msg.sender_name}</h4>
                    <p className="subject">{msg.subject}</p>
                    <p className="time">{new Date(msg.created_at).toLocaleDateString()}</p>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'compose' && (
            <div className="users-list">
              <h3>Select a recipient:</h3>
              {users.map(u => (
                <div
                  key={u.id}
                  className="user-item"
                  onClick={() => {
                    handleOpenConversation(u.id);
                    setActiveTab('inbox');
                  }}
                >
                  <p>{u.full_name || u.username}</p>
                  <span className="role">{u.role}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="messages-main">
          {selectedConversation ? (
            <>
              <div className="conversation">
                {conversation.length === 0 ? (
                  <p className="empty-conversation">No messages yet. Start a conversation!</p>
                ) : (
                  conversation.map(msg => (
                    <div
                      key={msg.id}
                      className={`message ${msg.sender_id === user.id ? 'sent' : 'received'}`}
                    >
                      <div className="message-header">
                        <strong>{msg.sender_id === user.id ? 'You' : msg.sender_name}</strong>
                        <span className="time">{new Date(msg.created_at).toLocaleString()}</span>
                      </div>
                      <p className="subject">{msg.subject}</p>
                      <p className="body">{msg.message_body}</p>
                    </div>
                  ))
                )}
              </div>

              <div className="compose-section">
                {!subject && (
                  <input
                    type="text"
                    placeholder="Subject"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    className="subject-input"
                  />
                )}
                <div className="message-input-group">
                  <textarea
                    placeholder="Type your message..."
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    rows="4"
                  />
                  <button onClick={handleSendMessage} className="btn btn-primary">
                    Send
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="no-selection">
              <p>Select a message or user to start chatting</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Messages;
