"use client";
import DailyLogForm from "@/components/DailyLogForm";

export default function LogPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Daily Log</h1>
      <DailyLogForm />
    </div>
  );
}
