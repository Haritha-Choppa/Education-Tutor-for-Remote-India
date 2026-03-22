import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './utils/authContext';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import LessonsList from './components/LessonsList';
import LessonDetail from './components/LessonDetail';
import QuizzesList from './components/QuizzesList';
import QuizAttempt from './components/QuizAttempt';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import './styles/global.css';

const Navigation = () => {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <nav className="app-nav">
      <div className="nav-inner">
        <Link className="brand" to="/dashboard">TutorFlow</Link>
        <ul>
          <li><Link to="/dashboard">Dashboard</Link></li>
          <li><Link to="/lessons">Lessons</Link></li>
          <li><Link to="/quizzes">Quizzes</Link></li>
        </ul>
        <div className="nav-user">
          <span>{user.full_name || user.username}</span>
          <button onClick={logout} className="logout-btn">Logout</button>
        </div>
      </div>
    </nav>
  );
};

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  return children;
};

const AppContent = () => {
  const { user } = useAuth();

  return (
    <>
      <Navigation />
      <main className="app-main">
        <div className="page-shell">
          <Routes>
            <Route
              path="/login"
              element={user ? <Navigate to="/dashboard" /> : <Login onSuccess={() => window.location.href = '/dashboard'} />}
            />
            <Route
              path="/register"
              element={user ? <Navigate to="/dashboard" /> : <Register onSuccess={() => window.location.href = '/dashboard'} />}
            />
            <Route
              path="/forgot-password"
              element={user ? <Navigate to="/dashboard" /> : <ForgotPassword />}
            />
            <Route
              path="/reset-password"
              element={user ? <Navigate to="/dashboard" /> : <ResetPassword />}
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lessons"
              element={
                <ProtectedRoute>
                  <LessonsList />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lessons/:lessonId"
              element={
                <ProtectedRoute>
                  <LessonDetail />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quizzes"
              element={
                <ProtectedRoute>
                  <QuizzesList />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quiz/:quizId"
              element={
                <ProtectedRoute>
                  <QuizAttempt />
                </ProtectedRoute>
              }
            />
            <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
          </Routes>
        </div>
      </main>
    </>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="app">
          <AppContent />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
