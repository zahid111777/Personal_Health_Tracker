"use client";
import MetricCard from "@/components/MetricCard";
import StreakCounter from "@/components/StreakCounter";
import InsightCard from "@/components/InsightCard";
import AnomalyAlert from "@/components/AnomalyAlert";
import GoalProgressRing from "@/components/GoalProgressRing";
import { useAnalyticsSummary, useAnomalies, useStreak } from "@/hooks/useAnalytics";
import { useInsightHistory } from "@/hooks/useInsights";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export default function DashboardPage() {
  const { data: summary } = useAnalyticsSummary(7);
  const { data: anomalies } = useAnomalies(7);
  const { data: streak } = useStreak();
  const { data: history } = useInsightHistory();
  const latestInsight = history?.[0];
  const { data: goals } = useQuery({
    queryKey: ["goals-progress"],
    queryFn: async () => (await api.get("/goals/progress")).data,
  });

  const metrics = summary
    ? Object.entries(summary).map(([key, val]: [string, any]) => ({
        key,
        label: key.replace(/_/g, " ").replace(/\b\w/g, (c: string) => c.toUpperCase()),
        value: val.latest,
        unit: key.includes("kg") ? "kg" : key.includes("bpm") ? "bpm" : key.includes("hours") ? "hrs" : key.includes("litres") ? "L" : "",
        trend: val.trend_direction,
        average: val.average,
      }))
    : [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {metrics.slice(0, 8).map((m) => (
          <MetricCard key={m.key} title={m.label} value={m.value} unit={m.unit} trend={m.trend} average={m.average} />
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StreakCounter streak={streak ?? 0} />
        {latestInsight && <InsightCard title="Latest Insight" content={latestInsight.content} />}
        {anomalies && anomalies.length > 0 && <AnomalyAlert anomalies={anomalies} />}
      </div>

      {goals && goals.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {goals.map((g: any) => (
            <GoalProgressRing key={g.goal.id} metric={g.goal.metric} goalType={g.goal.goal_type} targetValue={g.goal.target_value} currentValue={g.current_value ?? null} progress={g.progress_percentage ?? 0} onTrack={g.on_track ?? true} daysRemaining={g.days_remaining ?? null} />
          ))}
        </div>
      )}
    </div>
  );
}
