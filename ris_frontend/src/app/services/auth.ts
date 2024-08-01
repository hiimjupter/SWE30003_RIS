// services/auth.ts
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface User {
  username: string;
  full_name: string;
  gender: string;
  dob: string;
  created_at: string;
  is_active: boolean;
}

export async function login(username: string, password: string): Promise<void> {
  const response = await axios.post<LoginResponse>(
    `${API_URL}/login`,
    new URLSearchParams({ username, password }), // Send as form data
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
  if (response.status === 200) {
    localStorage.setItem('access_token', response.data.access_token);
  } else {
    throw new Error('Login failed');
  }
}

export async function getCurrentUser(): Promise<User> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('No token found');
  }

  const response = await axios.get<User>(`${API_URL}/users/me/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  return response.data;
}
