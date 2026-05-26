"use client";
import { useState } from "react";
import TrendLineChart from "@/components/TrendLineChart";
import CorrelationHeatmap from "@/components/CorrelationHeatmap";
import CalendarHeatmap from "@/components/CalendarHeatmap";
import { useMetricTrend, useCorrelations, useHeatmap } from "@/hooks/useAnalytics";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const metricOptions = [
  { value: "weight_kg", label: "Weight" },
  { value: "heart_rate_bpm", label: "Heart Rate" },
  { value: "sleep_hours", label: "Sleep Hours" },
  { value: "mood_score", label: "Mood" },
  { value: "energy_level", label: "Energy" },
  { value: "steps", label: "Steps" },
  { value: "water_litres", label: "Water" },
  { value: "exercise_minutes", label: "Exercise" },
];

export default function TrendsPage() {
  const [metric, setMetric] = useState("weight_kg");
  const [days, setDays] = useState("30");
  const { data: trend } = useMetricTrend(metric, parseInt(days));
  const { data: correlations } = useCorrelations(parseInt(days));
  const { data: heatmap } = useHeatmap(new Date().getFullYear());

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Trends & Analysis</h1>
        <div className="flex gap-2">
          <Select value={metric} onValueChange={(v) => v && setMetric(v)}>
            <SelectTrigger className="w-40"><SelectValue /></SelectTrigger>
            <SelectContent>
              {metricOptions.map((m) => <SelectItem key={m.value} value={m.value}>{m.label}</SelectItem>)}
            </SelectContent>
          </Select>
          <Select value={days} onValueChange={(v) => v && setDays(v)}>
            <SelectTrigger className="w-32"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="7">7 days</SelectItem>
              <SelectItem value="30">30 days</SelectItem>
              <SelectItem value="90">90 days</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {trend && (
        <TrendLineChart
          title={metricOptions.find((m) => m.value === metric)?.label || metric}
          data={trend.data || []}
          movingAverage={trend.moving_average || undefined}
          color="#0EA5E9"
        />
      )}

      {correlations?.matrix && <CorrelationHeatmap matrix={correlations.matrix} />}
      {heatmap && <CalendarHeatmap data={heatmap} year={new Date().getFullYear()} />}
    </div>
  );
}
