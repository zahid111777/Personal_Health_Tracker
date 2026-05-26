"use client";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export function useAnalyticsSummary(days: number = 30) {
  return useQuery({
    queryKey: ["analytics", "summary", days],
    queryFn: async () => {
      const res = await api.get(`/analytics/summary?days=${days}`);
      return res.data;
    },
  });
}

export function useMetricTrend(metric: string, days: number = 30) {
  return useQuery({
    queryKey: ["analytics", "metric", metric, days],
    queryFn: async () => {
      const res = await api.get(`/analytics/metric/${metric}?days=${days}`);
      return res.data;
    },
  });
}

export function useCorrelations(days: number = 60) {
  return useQuery({
    queryKey: ["analytics", "correlations", days],
    queryFn: async () => {
      const res = await api.get(`/analytics/correlations?days=${days}`);
      return res.data;
    },
  });
}

export function useAnomalies(days: number = 30) {
  return useQuery({
    queryKey: ["analytics", "anomalies", days],
    queryFn: async () => {
      const res = await api.get(`/analytics/anomalies?days=${days}`);
      return res.data;
    },
  });
}

export function useStreak() {
  return useQuery({
    queryKey: ["analytics", "streak"],
    queryFn: async () => {
      const res = await api.get("/analytics/streak");
      return res.data.streak as number;
    },
  });
}

export function useHeatmap(year: number) {
  return useQuery({
    queryKey: ["analytics", "heatmap", year],
    queryFn: async () => {
      const res = await api.get(`/analytics/heatmap?year=${year}`);
      return res.data;
    },
  });
}
