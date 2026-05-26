"use client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import api from "@/lib/api";
import { useQuery } from "@tanstack/react-query";

export default function ProviderStatus() {
  const { data: providers } = useQuery({
    queryKey: ["providers"],
    queryFn: async () => {
      const res = await api.get("/settings/providers");
      return res.data as Array<{ provider: string; is_configured: boolean; is_available: boolean }>;
    },
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm">LLM Provider Status</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        {providers?.map((p) => (
          <div key={p.provider} className="flex items-center justify-between">
            <span className="capitalize font-medium text-sm">{p.provider}</span>
            <Badge variant={p.is_configured ? "default" : "secondary"}>
              {p.is_configured ? "Configured" : "Not Set"}
            </Badge>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
