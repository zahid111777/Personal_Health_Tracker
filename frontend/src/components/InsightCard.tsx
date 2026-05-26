"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain } from "lucide-react";

interface InsightCardProps {
  title?: string;
  content: string;
  type?: string;
}

export default function InsightCard({ title, content, type }: InsightCardProps) {
  return (
    <Card className="bg-gradient-to-r from-sky-50 to-blue-50 border-sky-200">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-sky-700 flex items-center gap-2">
          <Brain className="h-4 w-4" />
          {title || type || "AI Insight"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-700 whitespace-pre-wrap">{content}</p>
      </CardContent>
    </Card>
  );
}
