import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { apiService } from '../utils/apiService';
import '../styles/lessons.css';

const LessonsList = () => {
  const [lessons, setLessons] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [grades, setGrades] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedGrade, setSelectedGrade] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [lessonsData, subjectsData, gradesData] = await Promise.all([
        apiService.getLessons(),
        apiService.getSubjects(),
        apiService.getGradeLevels()
      ]);
      
      setLessons(lessonsData);
      setSubjects(subjectsData || []);
      setGrades(gradesData || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const filteredLessons = useMemo(() => {
    let filtered = lessons;
    
    if (selectedSubject) {
      filtered = filtered.filter(lesson => lesson.subject === selectedSubject);
    }
    
    if (selectedGrade) {
      filtered = filtered.filter(lesson => lesson.grade_level === selectedGrade);
    }

    return filtered;
  }, [lessons, selectedSubject, selectedGrade]);

  const courseCards = useMemo(() => subjects.map(subject => ({
    subject,
    count: lessons.filter(lesson => lesson.subject === subject).length
  })), [subjects, lessons]);

  if (loading) {
    return <div className="loading">Loading lessons...</div>;
  }

  return (
    <div className="lessons-container">
      <h1>Available Lessons</h1>

      <section className="course-strip">
        <h2>Choose a Course</h2>
        <div className="course-grid">
          <button
            type="button"
            className={`course-card ${selectedSubject === '' ? 'active' : ''}`}
            onClick={() => setSelectedSubject('')}
          >
            <span className="course-title">All Courses</span>
            <span className="course-meta">{lessons.length} lessons</span>
          </button>

          {courseCards.map(course => (
            <button
              type="button"
              key={course.subject}
              className={`course-card ${selectedSubject === course.subject ? 'active' : ''}`}
              onClick={() => setSelectedSubject(course.subject)}
            >
              <span className="course-title">{course.subject}</span>
              <span className="course-meta">{course.count} lessons</span>
            </button>
          ))}
        </div>
      </section>
      
      <div className="filters">
        <div className="filter-group">
          <label htmlFor="subject">Subject:</label>
          <select 
            id="subject"
            value={selectedSubject} 
            onChange={(e) => setSelectedSubject(e.target.value)}
          >
            <option value="">All Subjects</option>
            {subjects.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="grade">Grade Level:</label>
          <select 
            id="grade"
            value={selectedGrade} 
            onChange={(e) => setSelectedGrade(e.target.value)}
          >
            <option value="">All Grades</option>
            {grades.map(grade => (
              <option key={grade} value={grade}>{grade}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="lessons-grid">
        {filteredLessons.length === 0 ? (
          <p className="no-results">No lessons found</p>
        ) : (
          filteredLessons.map(lesson => (
            <div key={lesson.id} className="lesson-card">
              <h3>{lesson.title}</h3>
              <p><strong>Subject:</strong> {lesson.subject}</p>
              <p><strong>Grade:</strong> {lesson.grade_level}</p>
              <p className="description">{lesson.description}</p>
              <a href={`/lessons/${lesson.id}`} className="btn-learn">
                Learn More
              </a>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LessonsList;
