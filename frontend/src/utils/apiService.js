import axios from 'axios';
import { OfflineStorage } from './offlineStorage';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL
});

// Offline support wrapper
const withOfflineSupport = async (apiCall, storageKey, fallbackData = []) => {
  try {
    // Try to make the API call
    const response = await apiCall();
    // Cache the successful response
    if (storageKey) {
      localStorage.setItem(storageKey, JSON.stringify(response.data));
    }
    return response.data;
  } catch (error) {
    // If the API call fails, return cached data
    if (storageKey) {
      const cached = localStorage.getItem(storageKey);
      if (cached) {
        return JSON.parse(cached);
      }
    }
    return fallbackData;
  }
};

export const apiService = {
  // User APIs
  register: async (userData) => {
    const response = await api.post('/users/register', userData);
    OfflineStorage.setUser(response.data);
    return response.data;
  },
  
  login: async (username, password) => {
    const response = await api.post('/users/login', { username, password });
    OfflineStorage.setUser(response.data);
    return response.data;
  },

  requestPasswordReset: async (email) => {
    const response = await api.post('/users/forgot-password', { email });
    return response.data;
  },

  resetPassword: async (token, password, confirmPassword) => {
    const response = await api.post('/users/reset-password', {
      token,
      password,
      confirm_password: confirmPassword
    });
    return response.data;
  },
  
  updateUser: async (userId, userData) => {
    const response = await api.put(`/users/${userId}`, userData);
    OfflineStorage.setUser(response.data);
    return response.data;
  },
  
  getAllUsers: async (role = null) => {
    const params = role ? { role } : {};
    return withOfflineSupport(
      () => api.get('/users/all', { params }),
      'allUsers',
      []
    );
  },
  
  // Lesson APIs
  getLessons: async (subject = null, gradeLevel = null) => {
    const params = {};
    if (subject) params.subject = subject;
    if (gradeLevel) params.grade_level = gradeLevel;
    
    return withOfflineSupport(
      () => api.get('/lessons', { params }),
      'lessons',
      []
    );
  },
  
  getLesson: async (lessonId) => {
    return withOfflineSupport(
      () => api.get(`/lessons/${lessonId}`),
      `lesson_${lessonId}`
    );
  },
  
  createLesson: async (lessonData) => {
    const response = await api.post('/lessons', lessonData);
    OfflineStorage.setLesson(response.data);
    return response.data;
  },
  
  updateLesson: async (lessonId, lessonData) => {
    const response = await api.put(`/lessons/${lessonId}`, lessonData);
    OfflineStorage.setLesson(response.data);
    return response.data;
  },
  
  getSubjects: async () => {
    return withOfflineSupport(
      () => api.get('/lessons/subjects'),
      'subjects',
      []
    );
  },
  
  getGradeLevels: async () => {
    return withOfflineSupport(
      () => api.get('/lessons/grade-levels'),
      'gradeLevels',
      []
    );
  },
  
  // Quiz APIs
  getQuizzes: async (lessonId = null) => {
    const params = lessonId ? { lesson_id: lessonId } : {};
    return withOfflineSupport(
      () => api.get('/quizzes', { params }),
      'quizzes',
      []
    );
  },
  
  getQuiz: async (quizId) => {
    return withOfflineSupport(
      () => api.get(`/quizzes/${quizId}`),
      `quiz_${quizId}`
    );
  },
  
  createQuiz: async (quizData) => {
    const response = await api.post('/quizzes', quizData);
    OfflineStorage.setQuiz(response.data);
    return response.data;
  },
  
  submitQuiz: async (quizId, userId, answers) => {
    const response = await api.post(`/quizzes/${quizId}/submit`, {
      user_id: userId,
      answers
    });
    OfflineStorage.addQuizAttempt(response.data);
    return response.data;
  },
  
  getUserQuizAttempts: async (userId) => {
    return withOfflineSupport(
      () => api.get(`/quizzes/attempts/${userId}`),
      `quizAttempts_${userId}`,
      []
    );
  },
  
  // Progress APIs
  createOrUpdateProgress: async (progressData) => {
    const response = await api.post('/progress', progressData);
    OfflineStorage.setProgress(response.data);
    return response.data;
  },
  
  getUserProgress: async (userId) => {
    return withOfflineSupport(
      () => api.get(`/progress/${userId}`),
      `userProgress_${userId}`,
      []
    );
  },
  
  getUserStats: async (userId) => {
    return withOfflineSupport(
      () => api.get(`/progress/stats/${userId}`),
      `userStats_${userId}`
    );
  },
  
  // Message APIs
  sendMessage: async (messageData) => {
    const response = await api.post('/messages', messageData);
    OfflineStorage.addMessage(response.data);
    return response.data;
  },
  
  getInbox: async (userId) => {
    return withOfflineSupport(
      () => api.get(`/messages/inbox/${userId}`),
      `inbox_${userId}`,
      []
    );
  },
  
  getSentMessages: async (userId) => {
    return withOfflineSupport(
      () => api.get(`/messages/sent/${userId}`),
      `sentMessages_${userId}`,
      []
    );
  },
  
  getConversation: async (userId, otherUserId) => {
    return withOfflineSupport(
      () => api.get(`/messages/conversation/${userId}/${otherUserId}`),
      `conversation_${userId}_${otherUserId}`,
      []
    );
  },
  
  markMessageAsRead: async (messageId) => {
    return api.put(`/messages/${messageId}/mark-read`);
  }
};
