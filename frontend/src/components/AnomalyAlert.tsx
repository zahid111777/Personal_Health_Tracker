"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTriangle } from "lucide-react";

interface AnomalyAlertProps {
  anomalies: Array<{
    date: string;
    metric: string;
    value: number;
    expected_range: string;
    severity: string;
  }>;
}

const metricLabels: Record<string, string> = {
  weight_kg: "Weight", systolic_bp: "Systolic BP", diastolic_bp: "Diastolic BP",
  heart_rate_bpm: "Heart Rate", sleep_hours: "Sleep", sleep_quality: "Sleep Quality",
  mood_score: "Mood", energy_level: "Energy", water_litres: "Water",
  steps: "Steps", calories_consumed: "Calories", exercise_minutes: "Exercise",
};

export default function AnomalyAlert({ anomalies }: AnomalyAlertProps) {
  if (!anomalies || anomalies.length === 0) return null;

  return (
    <Card className="border-red-200 bg-red-50">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-red-700 flex items-center gap-2">
          <AlertTriangle className="h-4 w-4" />
          Anomalies Detected
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        {anomalies.slice(0, 5).map((a, i) => (
          <div key={i} className="text-sm text-red-600">
            <span className="font-medium">{metricLabels[a.metric] || a.metric}</span> on {a.date}:{" "}
            <span className="font-bold">{a.value}</span> (expected: {a.expected_range})
            {a.severity === "high" && <span className="ml-1 text-xs bg-red-200 px-1 rounded">HIGH</span>}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
