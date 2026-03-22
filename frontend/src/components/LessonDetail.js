import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../utils/authContext';
import { apiService } from '../utils/apiService';
import '../styles/lesson-detail.css';

const LessonDetail = () => {
  const { lessonId } = useParams();
  const { user } = useAuth();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [completionPercentage, setCompletionPercentage] = useState(0);

  const loadLesson = useCallback(async () => {
    try {
      setLoading(true);
      const lessonData = await apiService.getLesson(lessonId);
      setLesson(lessonData);
    } catch (error) {
      console.error('Error loading lesson:', error);
    } finally {
      setLoading(false);
    }
  }, [lessonId]);

  const loadProgress = useCallback(async () => {
    if (!user) return;

    try {
      const userProgress = await apiService.getUserProgress(user.id);
      const lessonProgress = userProgress.find(p => p.lesson_id === parseInt(lessonId, 10));
      if (lessonProgress) {
        setCompletionPercentage(lessonProgress.completion_percentage);
      }
    } catch (error) {
      console.error('Error loading progress:', error);
    }
  }, [user, lessonId]);

  useEffect(() => {
    loadLesson();
    if (user) {
      loadProgress();
    }
  }, [user, loadLesson, loadProgress]);

  const handleMarkComplete = async () => {
    if (!user) return;
    
    try {
      await apiService.createOrUpdateProgress({
        user_id: user.id,
        lesson_id: parseInt(lessonId, 10),
        completion_percentage: 100,
        is_completed: true,
        time_spent: completionPercentage > 0 ? 3600 : 0 // Mock time spent
      });
      setCompletionPercentage(100);
      loadProgress();
    } catch (error) {
      console.error('Error updating progress:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading lesson...</div>;
  }

  if (!lesson) {
    return <div className="error">Lesson not found</div>;
  }

  return (
    <div className="lesson-detail">
      <div className="lesson-header">
        <h1>{lesson.title}</h1>
        <div className="lesson-meta">
          <span className="subject">{lesson.subject}</span>
          <span className="grade">{lesson.grade_level}</span>
        </div>
      </div>

      {user && (
        <div className="progress-section">
          <h3>Your Progress</h3>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${completionPercentage}%` }}
            ></div>
          </div>
          <p>{completionPercentage}% Complete</p>
        </div>
      )}

      <div className="lesson-content">
        <h2>Content</h2>
        <div className="content-text">
          {lesson.content || 'No content available'}
        </div>

        {lesson.video_url && (
          <div className="video-section">
            <h3>Video Tutorial</h3>
            <p className="video-notice">Video: {lesson.video_url}</p>
            <p className="note">Note: Video playback depends on offline availability</p>
          </div>
        )}

        {lesson.practice_problems && lesson.practice_problems.length > 0 && (
          <div className="practice-section">
            <h3>Practice Problems ({lesson.practice_problems.length})</h3>
            <div className="problems-list">
              {lesson.practice_problems.map((problem, index) => (
                <div key={problem.id} className="problem-item">
                  <h4>Problem {index + 1}</h4>
                  <p className="question">{problem.question}</p>
                  {problem.options && (
                    <ul className="options">
                      {problem.options.map((option, idx) => (
                        <li key={idx}>{option}</li>
                      ))}
                    </ul>
                  )}
                  <details className="answer-detail">
                    <summary>Show Answer</summary>
                    <div className="answer">
                      <p><strong>Answer:</strong> {problem.correct_answer}</p>
                      {problem.explanation && (
                        <p><strong>Explanation:</strong> {problem.explanation}</p>
                      )}
                    </div>
                  </details>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {user && (
        <div className="lesson-actions">
          <p className="complete-note">Final step: after reading the full topic and solving questions, click Mark as Complete.</p>
          <button 
            onClick={handleMarkComplete}
            className="btn btn-primary"
            disabled={completionPercentage === 100}
          >
            {completionPercentage === 100 ? 'Completed' : 'Mark as Complete'}
          </button>
        </div>
      )}
    </div>
  );
};

export default LessonDetail;
