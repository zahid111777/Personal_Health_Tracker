"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CorrelationHeatmapProps {
  matrix: Record<string, Record<string, number | null>>;
}

const metricLabels: Record<string, string> = {
  weight_kg: "Weight", systolic_bp: "Sys BP", diastolic_bp: "Dia BP",
  heart_rate_bpm: "HR", sleep_hours: "Sleep", sleep_quality: "SQ",
  mood_score: "Mood", energy_level: "Energy", water_litres: "Water",
  steps: "Steps", calories_consumed: "Cal", exercise_minutes: "Exercise",
};

function getColor(value: number | null): string {
  if (value === null) return "#f3f4f6";
  if (value >= 0.6) return "#22c55e";
  if (value >= 0.3) return "#86efac";
  if (value >= 0) return "#f0fdf4";
  if (value >= -0.3) return "#fef2f2";
  if (value >= -0.6) return "#fca5a5";
  return "#ef4444";
}

export default function CorrelationHeatmap({ matrix }: CorrelationHeatmapProps) {
  const metrics = Object.keys(matrix);
  if (metrics.length === 0) {
    return (
      <Card>
        <CardHeader><CardTitle className="text-sm">Correlation Matrix</CardTitle></CardHeader>
        <CardContent><p className="text-sm text-gray-500">Not enough data for correlations yet.</p></CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader><CardTitle className="text-sm font-medium text-gray-600">Correlation Matrix</CardTitle></CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="text-xs">
          <thead>
            <tr>
              <th />
              {metrics.map((m) => (
                <th key={m} className="px-1 py-1 text-gray-500 font-normal rotate-45 origin-bottom-left">
                  {metricLabels[m] || m}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metrics.map((m1) => (
              <tr key={m1}>
                <td className="pr-2 text-gray-500 font-medium">{metricLabels[m1] || m1}</td>
                {metrics.map((m2) => {
                  const val = matrix[m1]?.[m2];
                  return (
                    <td
                      key={m2}
                      className="w-10 h-10 text-center border"
                      style={{ backgroundColor: getColor(val) }}
                      title={`${m1} ↔ ${m2}: ${val ?? "N/A"}`}
                    >
                      {val !== null && val !== undefined ? val.toFixed(2) : ""}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
