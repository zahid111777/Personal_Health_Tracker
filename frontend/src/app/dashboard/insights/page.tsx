"use client";
import HealthQAChat from "@/components/HealthQAChat";
import InsightCard from "@/components/InsightCard";
import { useWeeklySummary, useInsightHistory } from "@/hooks/useInsights";
import { Button } from "@/components/ui/button";

export default function InsightsPage() {
  const weekly = useWeeklySummary();
  const { data: history } = useInsightHistory();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">AI Insights</h1>
        <Button onClick={() => weekly.mutate()} disabled={weekly.isPending} variant="outline">
          {weekly.isPending ? "Generating..." : "Generate Weekly Summary"}
        </Button>
      </div>

      {weekly.data && <InsightCard title="This Week's Summary" content={weekly.data.summary} />}

      <HealthQAChat />

      {history && history.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-lg font-semibold text-gray-700">Past Insights</h2>
          {history.map((h: any, i: number) => (
            <InsightCard key={i} title={h.insight_type} content={h.content} />
          ))}
        </div>
      )}
    </div>
  );
}
