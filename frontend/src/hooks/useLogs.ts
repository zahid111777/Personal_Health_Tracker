"use client";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export interface HealthLog {
  id: number;
  user_id: number;
  log_date: string;
  weight_kg: number | null;
  systolic_bp: number | null;
  diastolic_bp: number | null;
  heart_rate_bpm: number | null;
  sleep_hours: number | null;
  sleep_quality: number | null;
  mood_score: number | null;
  energy_level: number | null;
  water_litres: number | null;
  steps: number | null;
  calories_consumed: number | null;
  exercise_minutes: number | null;
  notes: string | null;
  created_at: string;
}

export function useLogs(startDate?: string, endDate?: string) {
  return useQuery({
    queryKey: ["logs", startDate, endDate],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (startDate) params.set("start_date", startDate);
      if (endDate) params.set("end_date", endDate);
      const res = await api.get(`/logs?${params}`);
      return res.data as HealthLog[];
    },
  });
}

export function useTodayLog() {
  return useQuery({
    queryKey: ["logs", "today"],
    queryFn: async () => {
      const res = await api.get("/logs/today");
      return res.data as HealthLog | null;
    },
  });
}

export function useCreateLog() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<HealthLog>) => {
      const res = await api.post("/logs", data);
      return res.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["logs"] });
      qc.invalidateQueries({ queryKey: ["analytics"] });
    },
  });
}

export function useUpdateLog() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<HealthLog> }) => {
      const res = await api.put(`/logs/${id}`, data);
      return res.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["logs"] });
      qc.invalidateQueries({ queryKey: ["analytics"] });
    },
  });
}

export function useDeleteLog() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/logs/${id}`);
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["logs"] });
    },
  });
}
