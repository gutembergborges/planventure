const BASE_URL = 'http://127.0.0.1:5000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  };
};

const handleResponse = async (response) => {
  const data = await response.json().catch(() => null);

  if (response.status === 401) {
    const isLoginRequest = response.url && response.url.includes('/auth/login');

    if (isLoginRequest) {
      throw new Error(data?.error || 'Invalid email or password');
    }

    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Session expired. Please login again.');
  }

  if (!response.ok) {
    throw new Error(data?.error || data?.message || 'Request failed');
  }

  return data;
};

export const api = {
  get: async (endpoint) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },
  
  post: async (endpoint, data) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  put: async (endpoint, data) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  auth: {
    login: async (credentials) => {
      return api.post('/auth/login', credentials);
    },

    register: async (userData) => {
      return api.post('/auth/register', userData);
    }
  }
};

export default api;