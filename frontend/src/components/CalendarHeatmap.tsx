"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CalendarHeatmapProps {
  data: Record<string, boolean>;
  year: number;
}

export default function CalendarHeatmap({ data, year }: CalendarHeatmapProps) {
  const startDate = new Date(year, 0, 1);
  const endDate = new Date(year, 11, 31);
  const days: Date[] = [];
  const current = new Date(startDate);
  while (current <= endDate) {
    days.push(new Date(current));
    current.setDate(current.getDate() + 1);
  }

  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">Log Frequency — {year}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex gap-0.5 flex-wrap">
          {days.map((day) => {
            const key = day.toISOString().split("T")[0];
            const logged = data[key];
            const today = new Date();
            const isPast = day <= today;
            return (
              <div
                key={key}
                className="w-3 h-3 rounded-sm"
                style={{
                  backgroundColor: logged ? "#22c55e" : isPast ? "#e5e7eb" : "#f9fafb",
                }}
                title={`${key}: ${logged ? "Logged" : "No log"}`}
              />
            );
          })}
        </div>
        <div className="flex gap-4 mt-2 text-xs text-gray-400">
          {months.map((m) => <span key={m}>{m}</span>)}
        </div>
      </CardContent>
    </Card>
  );
}
