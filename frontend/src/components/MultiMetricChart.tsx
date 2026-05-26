"use client";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface MultiMetricChartProps {
  title: string;
  data: Array<Record<string, unknown>>;
  metrics: Array<{ key: string; label: string; color: string }>;
}

export default function MultiMetricChart({ title, data, metrics }: MultiMetricChartProps) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip />
            <Legend />
            {metrics.map((m) => (
              <Line
                key={m.key} type="monotone" dataKey={m.key}
                stroke={m.color} strokeWidth={2} dot={{ r: 2 }}
                connectNulls={false} name={m.label}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
