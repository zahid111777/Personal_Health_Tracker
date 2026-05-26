"use client";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/lib/api";

export default function ProviderSettings() {
  const [testing, setTesting] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const handleTest = async (provider: string) => {
    setTesting(provider);
    setResult(null);
    try {
      const res = await api.post("/settings/providers/test", { provider });
      setResult(`${provider}: ${res.data.success ? "✓ Connected" : `✗ ${res.data.message}`}`);
    } catch {
      setResult(`${provider}: ✗ Failed`);
    } finally {
      setTesting(null);
    }
  };

  const providers = ["groq", "openrouter", "openai", "gemini"];

  return (
    <Card>
      <CardHeader>
        <CardTitle>LLM Provider Settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {providers.map((p) => (
          <div key={p} className="flex items-center gap-2">
            <Label className="w-24 capitalize">{p}</Label>
            <Button variant="outline" size="sm" onClick={() => handleTest(p)} disabled={testing === p}>
              {testing === p ? "Testing..." : "Test Connection"}
            </Button>
          </div>
        ))}
        {result && <p className="text-sm mt-2">{result}</p>}
      </CardContent>
    </Card>
  );
}
