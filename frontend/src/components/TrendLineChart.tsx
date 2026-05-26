"use client";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface TrendLineChartProps {
  title: string;
  data: Array<{ date: string; value: number }>;
  movingAverage?: Array<{ date: string; value: number }>;
  color?: string;
  unit?: string;
}

export default function TrendLineChart({ title, data, movingAverage, color = "#0EA5E9", unit }: TrendLineChartProps) {
  const merged = data.map((d, i) => ({
    date: d.date,
    value: d.value,
    ma: movingAverage?.[i]?.value,
  }));

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={merged}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} unit={unit ? ` ${unit}` : ""} />
            <Tooltip />
            <Legend />
            <Line
              type="monotone" dataKey="value" stroke={color}
              strokeWidth={2} dot={{ r: 3 }} connectNulls={false} name="Value"
            />
            {movingAverage && (
              <Line
                type="monotone" dataKey="ma" stroke="#94a3b8"
                strokeWidth={1.5} strokeDasharray="5 5" dot={false} name="7-day MA"
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
