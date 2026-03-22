import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../utils/authContext';
import { apiService } from '../utils/apiService';
import '../styles/quiz.css';

const QuizAttempt = () => {
  const { quizId } = useParams();
  const { user } = useAuth();
  const [quiz, setQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitError, setSubmitError] = useState('');

  const loadQuiz = useCallback(async () => {
    try {
      setLoading(true);
      const quizData = await apiService.getQuiz(quizId);
      setQuiz(quizData);
      // Initialize answers object
      const initialAnswers = {};
      quizData.questions?.forEach(q => {
        initialAnswers[q.id] = '';
      });
      setAnswers(initialAnswers);
    } catch (error) {
      console.error('Error loading quiz:', error);
    } finally {
      setLoading(false);
    }
  }, [quizId]);

  useEffect(() => {
    loadQuiz();
  }, [loadQuiz]);

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleSubmit = async () => {
    if (!user) return;

    setSubmitError('');

    try {
      const submitAnswers = Object.entries(answers).map(([qId, answer]) => ({
        question_id: parseInt(qId, 10),
        answer: answer
      }));

      const resultData = await apiService.submitQuiz(quizId, user.id, submitAnswers);
      setResult(resultData);
      setSubmitted(true);
    } catch (error) {
      const message = error.response?.data?.error || 'Unable to submit quiz. Please try again.';
      setSubmitError(message);
    }
  };

  if (loading) {
    return <div className="loading">Loading quiz...</div>;
  }

  if (!quiz) {
    return <div className="error">Quiz not found</div>;
  }

  if (submitted && result) {
    return (
      <div className="quiz-result">
        <h1>Quiz Results</h1>
        <div className={`result-box ${result.passed ? 'passed' : 'failed'}`}>
          <h2>{result.passed ? 'Congratulations!' : 'Try Again'}</h2>
          <p className="score">Score: {result.percentage.toFixed(1)}%</p>
          <p className="points">Points: {result.score}</p>
          <p className="passing">Passing Score: {result.passing_score}%</p>
          <div className={`result-status ${result.passed ? 'success' : 'failure'}`}>
            {result.passed ? '✓ Passed' : '✗ Failed'}
          </div>
        </div>
        <div className="actions">
          <a href="/quizzes" className="btn btn-primary">Back to Quizzes</a>
          <button onClick={() => {
            setSubmitted(false);
            setCurrentQuestionIndex(0);
            loadQuiz();
          }} className="btn btn-secondary">
            Retake Quiz
          </button>
        </div>
      </div>
    );
  }

  const currentQuestion = quiz.questions?.[currentQuestionIndex];
  const totalQuestions = quiz.questions?.length || 0;

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h1>{quiz.title}</h1>
        <div className="quiz-info">
          <span>Question {currentQuestionIndex + 1} of {totalQuestions}</span>
          {quiz.time_limit && <span>Time Limit: {quiz.time_limit} minutes</span>}
        </div>
      </div>

      {currentQuestion && (
        <div className="quiz-question">
          <h2>{currentQuestion.question_text}</h2>
          
          {currentQuestion.question_type === 'multiple_choice' && currentQuestion.options && (
            <div className="options">
              {currentQuestion.options.map((option, index) => (
                <label key={index} className="option-label">
                  <input
                    type="radio"
                    name={`question_${currentQuestion.id}`}
                    value={option}
                    checked={answers[currentQuestion.id] === option}
                    onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                  />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.question_type === 'true_false' && (
            <div className="options">
              {['True', 'False'].map((option) => (
                <label key={option} className="option-label">
                  <input
                    type="radio"
                    name={`question_${currentQuestion.id}`}
                    value={option}
                    checked={answers[currentQuestion.id] === option}
                    onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                  />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.question_type === 'short_answer' && (
            <div className="answer-input">
              <input
                type="text"
                placeholder="Enter your answer"
                value={answers[currentQuestion.id] || ''}
                onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
              />
            </div>
          )}
        </div>
      )}

      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${((currentQuestionIndex + 1) / totalQuestions) * 100}%` }}
        ></div>
      </div>

      <div className="quiz-navigation">
        {submitError && <div className="error-message">{submitError}</div>}
        <button
          onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
          disabled={currentQuestionIndex === 0}
          className="btn btn-secondary"
        >
          Previous
        </button>

        {currentQuestionIndex < totalQuestions - 1 ? (
          <button
            onClick={() => setCurrentQuestionIndex(currentQuestionIndex + 1)}
            className="btn btn-secondary"
          >
            Next
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            className="btn btn-primary"
          >
            Submit Quiz
          </button>
        )}
      </div>
    </div>
  );
};

export default QuizAttempt;
