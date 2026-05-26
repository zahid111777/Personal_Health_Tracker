"use client";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import api from "@/lib/api";

export default function ReportConfig() {
  const [days, setDays] = useState("30");
  const [doctorName, setDoctorName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ days });
      if (doctorName) params.set("doctor_name", doctorName);
      const res = await api.get(`/export/report?${params}`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "health_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      alert("Failed to generate report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Generate Health Report</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label>Period</Label>
          <Select value={days} onValueChange={(v) => v && setDays(v)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
              <SelectItem value="180">Last 6 months</SelectItem>
              <SelectItem value="365">Last year</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <Label>Doctor Name (optional)</Label>
          <Input placeholder="Dr. Smith" value={doctorName} onChange={(e) => setDoctorName(e.target.value)} />
        </div>
        <Button onClick={handleGenerate} disabled={loading} className="w-full bg-sky-500 hover:bg-sky-600">
          {loading ? "Generating..." : "Download PDF Report"}
        </Button>
      </CardContent>
    </Card>
  );
}
