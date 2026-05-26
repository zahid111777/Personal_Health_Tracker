"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Flame } from "lucide-react";

interface StreakCounterProps {
  streak: number;
}

export default function StreakCounter({ streak }: StreakCounterProps) {
  return (
    <Card className="bg-gradient-to-r from-orange-50 to-amber-50 border-orange-200">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-orange-700">Logging Streak</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-2">
          <Flame className="h-8 w-8 text-orange-500" />
          <span className="text-3xl font-bold text-orange-600">{streak}</span>
          <span className="text-sm text-orange-500">day{streak !== 1 ? "s" : ""}</span>
        </div>
      </CardContent>
    </Card>
  );
}
