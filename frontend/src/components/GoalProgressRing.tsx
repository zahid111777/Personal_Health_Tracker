"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Target } from "lucide-react";

interface GoalProgressRingProps {
  metric: string;
  goalType: string;
  targetValue: number;
  currentValue: number | null;
  progress: number;
  onTrack: boolean;
  daysRemaining: number | null;
}

const metricLabels: Record<string, string> = {
  weight_kg: "Weight (kg)", sleep_hours: "Sleep (hrs)", steps: "Steps",
  water_litres: "Water (L)", mood_score: "Mood", exercise_minutes: "Exercise (min)",
};

export default function GoalProgressRing({
  metric, goalType, targetValue, currentValue, progress, onTrack, daysRemaining,
}: GoalProgressRingProps) {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (Math.min(progress, 100) / 100) * circumference;
  const color = onTrack ? "#10B981" : "#EAB308";

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
          <Target className="h-4 w-4" />
          {metricLabels[metric] || metric} — {goalType}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex items-center gap-4">
        <svg width="100" height="100" className="transform -rotate-90">
          <circle cx="50" cy="50" r={radius} stroke="#e5e7eb" strokeWidth="8" fill="none" />
          <circle
            cx="50" cy="50" r={radius}
            stroke={color} strokeWidth="8" fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-500"
          />
        </svg>
        <div>
          <p className="text-2xl font-bold" style={{ color }}>{Math.round(progress)}%</p>
          <p className="text-xs text-gray-500">
            Current: {currentValue ?? "—"} / Target: {targetValue}
          </p>
          {daysRemaining !== null && (
            <p className="text-xs text-gray-400">{daysRemaining} days left</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
