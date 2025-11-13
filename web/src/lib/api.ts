import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// Request interceptor to add JWT token to all requests
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear token and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');

      // Only redirect if not already on auth page
      if (typeof window !== 'undefined' && !window.location.pathname.includes('/auth/')) {
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// Type definitions for API responses
export interface LoginRequest {
  username: string; // API expects username (can be email)
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
  profile_picture?: string | null;
  notification_preferences?: any;
  user_preferences?: any;
  role?: string;
  google_id?: string | null;
}

export interface Risk {
  id: number;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  probability: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'mitigated' | 'closed';
  mitigation_plan: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface RiskCreate {
  title: string;
  description: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  probability?: 'low' | 'medium' | 'high';
  impact?: 'low' | 'medium' | 'high' | 'critical';
  status?: 'open' | 'mitigated' | 'closed';
  mitigation_plan: string;
}

export interface RiskUpdate {
  title?: string;
  description?: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  probability?: 'low' | 'medium' | 'high';
  impact?: 'low' | 'medium' | 'high' | 'critical';
  status?: 'open' | 'mitigated' | 'closed';
  mitigation_plan?: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'done' | 'blocked';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date: string | null;
  completed: boolean;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'done' | 'blocked';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: 'todo' | 'in_progress' | 'done' | 'blocked';
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string | null;
  completed?: boolean;
}

export interface AnalyticsTotals {
  total_tasks: number;
  completed_tasks: number;
  total_risks: number;
  open_risks: number;
  ai_requests_count: number;
  completion_rate: number;
  velocity: number;
  average_lead_time: number;
  risk_score: number;
}

export interface BurndownDataPoint {
  date: string;
  remaining_tasks: number;
  completed_tasks: number;
}

export interface BurndownChart {
  data_points: BurndownDataPoint[];
}

export interface RiskDistribution {
  low: number;
  medium: number;
  high: number;
  critical: number;
}

export interface VelocityDataPoint {
  week: string;
  tasks_completed: number;
  average: number;
}

export interface AnalyticsResponse {
  totals: AnalyticsTotals;
  burndown: BurndownChart;
  risk_distribution: RiskDistribution;
  velocity_data: VelocityDataPoint[];
}

// API service functions
export const authAPI = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    // FastAPI expects form data for OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await api.post<LoginResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  register: async (userData: RegisterRequest): Promise<User> => {
    const response = await api.post<User>('/auth/register', userData);
    return response.data;
  },

  verify: async (): Promise<User> => {
    const response = await api.post<User>('/auth/verify');
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/users/me');
    return response.data;
  },
};

export const risksAPI = {
  getAll: async (skip = 0, limit = 100): Promise<Risk[]> => {
    const response = await api.get<Risk[]>('/risks', {
      params: { skip, limit },
    });
    return response.data;
  },

  getById: async (id: number): Promise<Risk> => {
    const response = await api.get<Risk>(`/risks/${id}`);
    return response.data;
  },

  create: async (risk: RiskCreate): Promise<Risk> => {
    const response = await api.post<Risk>('/risks', risk);
    return response.data;
  },

  update: async (id: number, risk: RiskUpdate): Promise<Risk> => {
    const response = await api.put<Risk>(`/risks/${id}`, risk);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/risks/${id}`);
  },
};

export const tasksAPI = {
  getAll: async (skip = 0, limit = 100): Promise<Task[]> => {
    const response = await api.get<Task[]>('/tasks', {
      params: { skip, limit },
    });
    return response.data;
  },

  getById: async (id: number): Promise<Task> => {
    const response = await api.get<Task>(`/tasks/${id}`);
    return response.data;
  },

  create: async (task: TaskCreate): Promise<Task> => {
    const response = await api.post<Task>('/tasks', task);
    return response.data;
  },

  update: async (id: number, task: TaskUpdate): Promise<Task> => {
    const response = await api.put<Task>(`/tasks/${id}`, task);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },
};

export const analyticsAPI = {
  getDashboard: async (): Promise<AnalyticsResponse> => {
    const response = await api.get<AnalyticsResponse>('/analytics');
    return response.data;
  },
};

// AI Request types
export interface AIRequest {
  id: number;
  user_id: number;
  request_type: string;
  prompt: string;
  response: any;
  tokens_used: number;
  created_at: string;
}

export interface AIGenerateRequest {
  request_type: string;
  prompt: string;
  model?: string;
}

export interface AIGenerateResponse {
  success: boolean;
  data: any;
  tokens_used: number;
  request_type: string;
}

export const aiAPI = {
  getHistory: async (skip = 0, limit = 20): Promise<AIRequest[]> => {
    const response = await api.get<AIRequest[]>('/ai/history', {
      params: { skip, limit },
    });
    return response.data;
  },

  generate: async (request: AIGenerateRequest): Promise<AIGenerateResponse> => {
    const response = await api.post<AIGenerateResponse>('/ai/generate', request);
    return response.data;
  },
};

// Project types and API
export interface Project {
  id: number;
  name: string;
  description: string;
  status: 'active' | 'completed' | 'on_hold' | 'cancelled';
  progress: number;
  due_date: string | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status?: string;
  progress?: number;
  due_date?: string | null;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  status?: string;
  progress?: number;
  due_date?: string | null;
}

export const projectsAPI = {
  getAll: async (skip = 0, limit = 100): Promise<Project[]> => {
    const response = await api.get<Project[]>('/projects', {
      params: { skip, limit },
    });
    return response.data;
  },

  getById: async (id: number): Promise<Project> => {
    const response = await api.get<Project>(`/projects/${id}`);
    return response.data;
  },

  create: async (project: ProjectCreate): Promise<Project> => {
    const response = await api.post<Project>('/projects', project);
    return response.data;
  },

  update: async (id: number, project: ProjectUpdate): Promise<Project> => {
    const response = await api.put<Project>(`/projects/${id}`, project);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/projects/${id}`);
  },
};

// Post types and API
export interface Post {
  id: number;
  title: string;
  content: string;
  caption: string | null;
  hashtags: string | null;
  likes: number;
  comments: number;
  shares: number;
  engagement_rate: number;
  project_id: number | null;
  user_id: number;
  published_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface PostCreate {
  title: string;
  content: string;
  caption?: string;
  hashtags?: string;
  likes?: number;
  comments?: number;
  shares?: number;
  engagement_rate?: number;
  project_id?: number | null;
  published_at?: string | null;
}

export interface PostUpdate {
  title?: string;
  content?: string;
  caption?: string;
  hashtags?: string;
  likes?: number;
  comments?: number;
  shares?: number;
  engagement_rate?: number;
  project_id?: number | null;
  published_at?: string | null;
}

export const postsAPI = {
  getAll: async (skip = 0, limit = 100): Promise<Post[]> => {
    const response = await api.get<Post[]>('/posts', {
      params: { skip, limit },
    });
    return response.data;
  },

  getById: async (id: number): Promise<Post> => {
    const response = await api.get<Post>(`/posts/${id}`);
    return response.data;
  },

  create: async (post: PostCreate): Promise<Post> => {
    const response = await api.post<Post>('/posts', post);
    return response.data;
  },

  update: async (id: number, post: PostUpdate): Promise<Post> => {
    const response = await api.put<Post>(`/posts/${id}`, post);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/posts/${id}`);
  },
};

// Auth API additions
export const authRefreshAPI = {
  refresh: async (refreshToken: string): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};
