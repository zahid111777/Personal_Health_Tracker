"use client";
import { useState } from "react";
import GoalProgressRing from "@/components/GoalProgressRing";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

const validMetrics = ["weight_kg", "sleep_hours", "steps", "water_litres", "exercise_minutes", "mood_score", "energy_level", "heart_rate_bpm", "calories_consumed"];
const goalTypes = ["reach", "maintain", "minimum", "maximum"];

export default function GoalsPage() {
  const qc = useQueryClient();
  const { data: goals } = useQuery({ queryKey: ["goals-progress"], queryFn: async () => (await api.get("/goals/progress")).data });
  const [form, setForm] = useState({ metric: "steps", goal_type: "reach", target_value: "", start_date: new Date().toISOString().split("T")[0], target_date: "" });
  const [error, setError] = useState("");

  const create = useMutation({
    mutationFn: async (data: any) => (await api.post("/goals", data)).data,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["goals-progress"] }); setForm({ metric: "steps", goal_type: "reach", target_value: "", start_date: new Date().toISOString().split("T")[0], target_date: "" }); },
    onError: (err: any) => setError(err.response?.data?.detail || "Failed"),
  });

  const remove = useMutation({
    mutationFn: async (id: number) => api.delete(`/goals/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["goals-progress"] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Goals</h1>

      <Card className="max-w-md">
        <CardHeader><CardTitle className="text-sm">Add Goal</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div>
            <Label>Metric</Label>
            <Select value={form.metric} onValueChange={(v) => v && setForm({ ...form, metric: v })}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>{validMetrics.map((m) => <SelectItem key={m} value={m}>{m.replace(/_/g, " ")}</SelectItem>)}</SelectContent>
            </Select>
          </div>
          <div>
            <Label>Type</Label>
            <Select value={form.goal_type} onValueChange={(v) => v && setForm({ ...form, goal_type: v })}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>{goalTypes.map((t) => <SelectItem key={t} value={t}>{t}</SelectItem>)}</SelectContent>
            </Select>
          </div>
          <div>
            <Label>Target Value</Label>
            <Input type="number" value={form.target_value} onChange={(e) => setForm({ ...form, target_value: e.target.value })} />
          </div>
          <div>
            <Label>Start Date</Label>
            <Input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
          </div>
          <div>
            <Label>Target Date (optional)</Label>
            <Input type="date" value={form.target_date} onChange={(e) => setForm({ ...form, target_date: e.target.value })} />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <Button onClick={() => create.mutate({ metric: form.metric, goal_type: form.goal_type, target_value: parseFloat(form.target_value), start_date: form.start_date, ...(form.target_date ? { target_date: form.target_date } : {}) })} disabled={!form.target_value} className="w-full bg-sky-500 hover:bg-sky-600">
            Add Goal
          </Button>
        </CardContent>
      </Card>

      {goals && goals.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {goals.map((g: any) => (
            <div key={g.goal.id} className="relative">
              <GoalProgressRing metric={g.goal.metric} goalType={g.goal.goal_type} targetValue={g.goal.target_value} currentValue={g.current_value ?? null} progress={g.progress_percentage ?? 0} onTrack={g.on_track ?? true} daysRemaining={g.days_remaining ?? null} />
              <button onClick={() => remove.mutate(g.goal.id)} className="absolute top-2 right-2 text-gray-400 hover:text-red-500 text-xs">✕</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
