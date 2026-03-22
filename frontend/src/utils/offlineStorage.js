// Offline storage manager using localStorage
export const OfflineStorage = {
  // User data
  setUser: (user) => {
    localStorage.setItem('currentUser', JSON.stringify(user));
  },
  
  getUser: () => {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
  },
  
  clearUser: () => {
    localStorage.removeItem('currentUser');
  },
  
  // Lessons
  setLessons: (lessons) => {
    localStorage.setItem('lessons', JSON.stringify(lessons));
  },
  
  getLessons: () => {
    const lessons = localStorage.getItem('lessons');
    return lessons ? JSON.parse(lessons) : [];
  },
  
  setLesson: (lesson) => {
    const lessons = OfflineStorage.getLessons();
    const index = lessons.findIndex(l => l.id === lesson.id);
    if (index > -1) {
      lessons[index] = lesson;
    } else {
      lessons.push(lesson);
    }
    OfflineStorage.setLessons(lessons);
  },
  
  // Quizzes
  setQuizzes: (quizzes) => {
    localStorage.setItem('quizzes', JSON.stringify(quizzes));
  },
  
  getQuizzes: () => {
    const quizzes = localStorage.getItem('quizzes');
    return quizzes ? JSON.parse(quizzes) : [];
  },
  
  setQuiz: (quiz) => {
    const quizzes = OfflineStorage.getQuizzes();
    const index = quizzes.findIndex(q => q.id === quiz.id);
    if (index > -1) {
      quizzes[index] = quiz;
    } else {
      quizzes.push(quiz);
    }
    OfflineStorage.setQuizzes(quizzes);
  },
  
  // Progress
  setProgress: (progress) => {
    const progressList = OfflineStorage.getProgress();
    const index = progressList.findIndex(p => p.id === progress.id);
    if (index > -1) {
      progressList[index] = progress;
    } else {
      progressList.push(progress);
    }
    localStorage.setItem('progress', JSON.stringify(progressList));
  },
  
  getProgress: () => {
    const progress = localStorage.getItem('progress');
    return progress ? JSON.parse(progress) : [];
  },
  
  // Messages
  setMessages: (messages) => {
    localStorage.setItem('messages', JSON.stringify(messages));
  },
  
  getMessages: () => {
    const messages = localStorage.getItem('messages');
    return messages ? JSON.parse(messages) : [];
  },
  
  addMessage: (message) => {
    const messages = OfflineStorage.getMessages();
    messages.push(message);
    OfflineStorage.setMessages(messages);
  },
  
  // Quiz attempts
  setQuizAttempts: (attempts) => {
    localStorage.setItem('quizAttempts', JSON.stringify(attempts));
  },
  
  getQuizAttempts: () => {
    const attempts = localStorage.getItem('quizAttempts');
    return attempts ? JSON.parse(attempts) : [];
  },
  
  addQuizAttempt: (attempt) => {
    const attempts = OfflineStorage.getQuizAttempts();
    attempts.push(attempt);
    OfflineStorage.setQuizAttempts(attempts);
  }
};
