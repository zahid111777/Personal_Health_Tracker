import api from "./api";

export interface User {
  id: number;
  full_name: string;
  email: string;
  role: string;
  date_of_birth: string | null;
  gender: string | null;
  height_cm: number | null;
  preferred_provider: string;
  is_active: boolean;
  created_at: string;
}

export async function login(email: string, password: string) {
  const res = await api.post("/auth/login", { email, password });
  const { access_token, refresh_token } = res.data;
  localStorage.setItem("access_token", access_token);
  localStorage.setItem("refresh_token", refresh_token);
  return res.data;
}

export async function register(full_name: string, email: string, password: string) {
  const res = await api.post("/auth/register", { full_name, email, password });
  return res.data;
}

export async function getMe(): Promise<User> {
  const res = await api.get("/auth/me");
  return res.data;
}

export async function updateProfile(data: Partial<User>) {
  const res = await api.put("/auth/me", data);
  return res.data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/login";
}

export function isAuthenticated(): boolean {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem("access_token");
}
