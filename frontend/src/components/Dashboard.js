import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../utils/authContext';
import { apiService } from '../utils/apiService';
import '../styles/dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentLessons, setRecentLessons] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadDashboardData = useCallback(async () => {
    if (!user) return;

    try {
      setLoading(true);
      const [statsData, lessonsData] = await Promise.all([
        apiService.getUserStats(user.id),
        apiService.getUserProgress(user.id)
      ]);
      
      setStats(statsData);
      setRecentLessons(lessonsData.slice(0, 5));
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Welcome, {user?.full_name || user?.username}!</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Lessons</h3>
          <p className="stat-value">{stats?.total_lessons || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Completed Lessons</h3>
          <p className="stat-value">{stats?.completed_lessons || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Completion Rate</h3>
          <p className="stat-value">{Math.round(stats?.completion_rate || 0)}%</p>
        </div>
        <div className="stat-card">
          <h3>Total Time Spent</h3>
          <p className="stat-value">
            {Math.round((stats?.total_time_spent || 0) / 3600)} hours
          </p>
        </div>
      </div>

      <div className="recent-section">
        <h2>Recent Activity</h2>
        {recentLessons.length === 0 ? (
          <p>No lessons started yet. <a href="/lessons">Browse lessons</a></p>
        ) : (
          <div className="lessons-list">
            {recentLessons.map(lesson => (
              <div key={lesson.id} className="lesson-progress-item">
                <h4>Lesson ID: {lesson.lesson_id}</h4>
                <div className="mini-progress-bar">
                  <div 
                    className="mini-progress-fill" 
                    style={{ width: `${lesson.completion_percentage}%` }}
                  ></div>
                </div>
                <p>{lesson.completion_percentage}% Complete</p>
                {lesson.is_completed && <span className="badge-completed">✓ Completed</span>}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="quick-actions">
        <a href="/lessons" className="btn btn-primary">Browse Lessons</a>
        <a href="/quizzes" className="btn btn-secondary">Practice Quizzes</a>
        <a href="/lessons" className="btn btn-tertiary">Continue Learning</a>
      </div>
    </div>
  );
};

export default Dashboard;
