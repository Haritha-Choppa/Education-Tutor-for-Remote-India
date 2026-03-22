import React, { useState, useEffect, useCallback } from 'react';
import { apiService } from '../utils/apiService';
import '../styles/quizzes.css';

const QuizzesList = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [selectedLesson, setSelectedLesson] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const lessonsData = await apiService.getLessons();
      setLessons(lessonsData || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadAllQuizzes = useCallback(async () => {
    try {
      const quizzesData = await apiService.getQuizzes();
      setQuizzes(quizzesData || []);
    } catch (error) {
      console.error('Error loading quizzes:', error);
    }
  }, []);

  const loadQuizzesByLesson = useCallback(async () => {
    if (!selectedLesson) return;

    try {
      const quizzesData = await apiService.getQuizzes(selectedLesson);
      setQuizzes(quizzesData || []);
    } catch (error) {
      console.error('Error loading quizzes:', error);
    }
  }, [selectedLesson]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  useEffect(() => {
    if (selectedLesson) {
      loadQuizzesByLesson();
    } else {
      loadAllQuizzes();
    }
  }, [selectedLesson, loadQuizzesByLesson, loadAllQuizzes]);

  if (loading) {
    return <div className="loading">Loading quizzes...</div>;
  }

  return (
    <div className="quizzes-container">
      <h1>Practice Quizzes</h1>
      
      <div className="filter-section">
        <label htmlFor="lesson-filter">Filter by Lesson:</label>
        <select
          id="lesson-filter"
          value={selectedLesson}
          onChange={(e) => setSelectedLesson(e.target.value)}
        >
          <option value="">All Quizzes</option>
          {lessons.map(lesson => (
            <option key={lesson.id} value={lesson.id}>
              {lesson.title}
            </option>
          ))}
        </select>
      </div>

      <div className="quizzes-grid">
        {quizzes.length === 0 ? (
          <p className="no-results">No quizzes found</p>
        ) : (
          quizzes.map(quiz => (
            <div key={quiz.id} className="quiz-card">
              <h3>{quiz.title}</h3>
              <p className="description">{quiz.description}</p>
              <div className="quiz-info">
                <span><strong>Questions:</strong> {quiz.total_questions}</span>
                <span><strong>Pass:</strong> {quiz.passing_score}%</span>
                {quiz.time_limit && <span><strong>Time:</strong> {quiz.time_limit} min</span>}
              </div>
              <a href={`/quiz/${quiz.id}`} className="btn-take-quiz">
                Take Quiz
              </a>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default QuizzesList;
