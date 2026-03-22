import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../utils/apiService';
import '../styles/auth.css';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setIsLoading(true);

    try {
      const response = await apiService.requestPasswordReset(email);
      setMessage(response.message || 'If the email is registered, a reset link has been sent.');
      setEmail('');
    } catch (err) {
      setError(err.response?.data?.error || 'Unable to process request. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container login-view">
      <div className="auth-box">
        <h1>TutorFlow</h1>
        <p className="auth-subtitle">Reset your password securely</p>
        <h2>Forgot Password</h2>

        {error && <div className="error-message">{error}</div>}
        {message && <div className="success-message">{message}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Registered Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={isLoading} className="auth-submit-btn">
            {isLoading ? 'Sending link...' : 'Send Reset Link'}
          </button>
        </form>

        <p>
          Back to <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;
