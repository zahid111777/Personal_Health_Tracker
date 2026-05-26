"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number | null;
  unit?: string;
  trend?: string;
  average?: number;
  icon?: React.ReactNode;
}

export default function MetricCard({ title, value, unit, trend, average, icon }: MetricCardProps) {
  const trendIcon =
    trend === "increasing" ? <TrendingUp className="h-4 w-4 text-emerald-500" /> :
    trend === "decreasing" ? <TrendingDown className="h-4 w-4 text-red-500" /> :
    <Minus className="h-4 w-4 text-gray-400" />;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-gray-500">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-slate-800">
            {value !== null && value !== undefined ? value : "—"}
          </span>
          {unit && <span className="text-sm text-gray-500">{unit}</span>}
          {trend && <span className="ml-2">{trendIcon}</span>}
        </div>
        {average !== undefined && (
          <p className="text-xs text-gray-400 mt-1">7-day avg: {average}</p>
        )}
      </CardContent>
    </Card>
  );
}
