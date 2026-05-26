"use client";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export function useWeeklySummary() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const res = await api.post("/insights/weekly");
      return res.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["insights"] });
    },
  });
}

export function useQA() {
  return useMutation({
    mutationFn: async (question: string) => {
      const res = await api.post("/insights/qa", { question });
      return res.data;
    },
  });
}

export function useInsightHistory() {
  return useQuery({
    queryKey: ["insights", "history"],
    queryFn: async () => {
      const res = await api.get("/insights/history");
      return res.data;
    },
  });
}

export function useExplainCorrelations() {
  return useMutation({
    mutationFn: async () => {
      const res = await api.post("/insights/correlations");
      return res.data;
    },
  });
}
