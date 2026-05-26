"use client";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useCreateLog, useUpdateLog, useTodayLog } from "@/hooks/useLogs";
import { useRouter } from "next/navigation";

const moodEmojis = ["😢", "😞", "😕", "😐", "🙂", "😊", "😄", "😁", "🤩", "🥳"];

export default function DailyLogForm() {
  const router = useRouter();
  const todayLog = useTodayLog();
  const createLog = useCreateLog();
  const updateLog = useUpdateLog();
  const existing = todayLog.data;

  const today = new Date().toISOString().split("T")[0];
  const [form, setForm] = useState({
    log_date: today,
    weight_kg: "",
    systolic_bp: "",
    diastolic_bp: "",
    heart_rate_bpm: "",
    sleep_hours: "",
    sleep_quality: "",
    mood_score: "",
    energy_level: "",
    water_litres: "",
    steps: "",
    calories_consumed: "",
    exercise_minutes: "",
    notes: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    const data: Record<string, unknown> = { log_date: form.log_date };
    if (form.weight_kg) data.weight_kg = parseFloat(form.weight_kg);
    if (form.systolic_bp) data.systolic_bp = parseInt(form.systolic_bp);
    if (form.diastolic_bp) data.diastolic_bp = parseInt(form.diastolic_bp);
    if (form.heart_rate_bpm) data.heart_rate_bpm = parseInt(form.heart_rate_bpm);
    if (form.sleep_hours) data.sleep_hours = parseFloat(form.sleep_hours);
    if (form.sleep_quality) data.sleep_quality = parseInt(form.sleep_quality);
    if (form.mood_score) data.mood_score = parseInt(form.mood_score);
    if (form.energy_level) data.energy_level = parseInt(form.energy_level);
    if (form.water_litres) data.water_litres = parseFloat(form.water_litres);
    if (form.steps) data.steps = parseInt(form.steps);
    if (form.calories_consumed) data.calories_consumed = parseInt(form.calories_consumed);
    if (form.exercise_minutes) data.exercise_minutes = parseInt(form.exercise_minutes);
    if (form.notes) data.notes = form.notes;

    if (data.systolic_bp && data.diastolic_bp && (data.systolic_bp as number) <= (data.diastolic_bp as number)) {
      setError("Systolic must be greater than diastolic");
      return;
    }

    try {
      if (existing && form.log_date === today) {
        await updateLog.mutateAsync({ id: existing.id, data });
      } else {
        await createLog.mutateAsync(data);
      }
      setSuccess(true);
      setTimeout(() => router.push("/dashboard"), 1500);
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } } };
      setError(axiosErr.response?.data?.detail || "Failed to save log");
    }
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Daily Health Log</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <Label>Date</Label>
            <Input type="date" value={form.log_date} onChange={(e) => handleChange("log_date", e.target.value)} max={today} />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Weight (kg)</Label>
              <Input type="number" step="0.1" placeholder="75.0" value={form.weight_kg} onChange={(e) => handleChange("weight_kg", e.target.value)} />
            </div>
            <div>
              <Label>Heart Rate (bpm)</Label>
              <Input type="number" placeholder="72" value={form.heart_rate_bpm} onChange={(e) => handleChange("heart_rate_bpm", e.target.value)} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Systolic BP</Label>
              <Input type="number" placeholder="120" value={form.systolic_bp} onChange={(e) => handleChange("systolic_bp", e.target.value)} />
            </div>
            <div>
              <Label>Diastolic BP</Label>
              <Input type="number" placeholder="80" value={form.diastolic_bp} onChange={(e) => handleChange("diastolic_bp", e.target.value)} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Sleep Hours</Label>
              <Input type="number" step="0.5" min="0" max="12" placeholder="7.5" value={form.sleep_hours} onChange={(e) => handleChange("sleep_hours", e.target.value)} />
            </div>
            <div>
              <Label>Sleep Quality (1-5) ★</Label>
              <div className="flex gap-1 mt-1">
                {[1, 2, 3, 4, 5].map((v) => (
                  <button key={v} type="button" className={`px-3 py-1 rounded border text-sm ${form.sleep_quality === String(v) ? "bg-sky-500 text-white" : "bg-white"}`}
                    onClick={() => handleChange("sleep_quality", String(v))}>{v}★</button>
                ))}
              </div>
            </div>
          </div>

          <div>
            <Label>Mood (1-10)</Label>
            <div className="flex gap-1 mt-1 flex-wrap">
              {moodEmojis.map((emoji, i) => (
                <button key={i} type="button"
                  className={`w-10 h-10 rounded-lg border text-lg ${form.mood_score === String(i + 1) ? "bg-sky-100 border-sky-500 scale-110" : "bg-white"}`}
                  onClick={() => handleChange("mood_score", String(i + 1))}>{emoji}</button>
              ))}
            </div>
          </div>

          <div>
            <Label>Energy Level (1-10): {form.energy_level || "—"}</Label>
            <input type="range" min="1" max="10" value={form.energy_level || "5"} className="w-full mt-1"
              onChange={(e) => handleChange("energy_level", e.target.value)} />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label>Water (L)</Label>
              <Input type="number" step="0.1" placeholder="2.5" value={form.water_litres} onChange={(e) => handleChange("water_litres", e.target.value)} />
            </div>
            <div>
              <Label>Steps</Label>
              <Input type="number" placeholder="10000" value={form.steps} onChange={(e) => handleChange("steps", e.target.value)} />
            </div>
            <div>
              <Label>Exercise (min)</Label>
              <Input type="number" placeholder="30" value={form.exercise_minutes} onChange={(e) => handleChange("exercise_minutes", e.target.value)} />
            </div>
          </div>

          <div>
            <Label>Calories (optional)</Label>
            <Input type="number" placeholder="2000" value={form.calories_consumed} onChange={(e) => handleChange("calories_consumed", e.target.value)} />
          </div>

          <div>
            <Label>Notes</Label>
            <Textarea placeholder="How was your day?" value={form.notes} onChange={(e) => handleChange("notes", e.target.value)} />
          </div>

          {error && <p className="text-red-500 text-sm">{error}</p>}
          {success && <p className="text-emerald-500 text-sm font-medium">✓ Log saved successfully!</p>}

          <Button type="submit" className="w-full bg-sky-500 hover:bg-sky-600" disabled={createLog.isPending || updateLog.isPending}>
            {createLog.isPending || updateLog.isPending ? "Saving..." : existing ? "Update Log" : "Save Log"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
