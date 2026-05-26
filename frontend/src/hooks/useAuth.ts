"use client";
import { create } from "zustand";
import { User, getMe, logout as authLogout } from "@/lib/auth";

interface AuthState {
  user: User | null;
  loading: boolean;
  setUser: (user: User | null) => void;
  fetchUser: () => Promise<void>;
  logout: () => void;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  loading: true,
  setUser: (user) => set({ user, loading: false }),
  fetchUser: async () => {
    try {
      const user = await getMe();
      set({ user, loading: false });
    } catch {
      set({ user: null, loading: false });
    }
  },
  logout: () => {
    set({ user: null });
    authLogout();
  },
}));
