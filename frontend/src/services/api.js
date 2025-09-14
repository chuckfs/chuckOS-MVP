import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: async (email, password, fullName) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/user/profile');
    return response.data;
  },

  getSubscription: async () => {
    const response = await api.get('/user/subscription');
    return response.data;
  },
};

// File intelligence API
export const fileAPI = {
  search: async (query, filePaths = null, maxResults = 20) => {
    const response = await api.post('/files/search', {
      query,
      file_paths: filePaths,
      max_results: maxResults,
    });
    return response.data;
  },

  analyze: async (path = null) => {
    const params = path ? { path } : {};
    const response = await api.get('/files/analyze', { params });
    return response.data;
  },

  upload: async (files) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getInsights: async () => {
    const response = await api.get('/files/insights');
    return response.data;
  },

  organize: async (path = null, dryRun = true) => {
    const response = await api.post('/files/organize', {
      path,
      dry_run: dryRun,
    });
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};