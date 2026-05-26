"use client";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useQA } from "@/hooks/useInsights";
import { Send, MessageCircle } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const suggestedQuestions = [
  "Am I sleeping enough?",
  "What's affecting my mood?",
  "How is my BP trending?",
  "Am I drinking enough water?",
];

export default function HealthQAChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const qa = useQA();

  const handleSend = async (question?: string) => {
    const q = question || input.trim();
    if (!q) return;
    setMessages((prev) => [...prev, { role: "user", content: q }]);
    setInput("");
    try {
      const res = await qa.mutateAsync(q);
      setMessages((prev) => [...prev, { role: "assistant", content: res.answer }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't process that question." }]);
    }
  };

  return (
    <Card className="flex flex-col h-[500px]">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-gray-600 flex items-center gap-2">
          <MessageCircle className="h-4 w-4" /> Ask About Your Health Data
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col flex-1 overflow-hidden">
        {messages.length === 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {suggestedQuestions.map((q) => (
              <Button key={q} variant="outline" size="sm" onClick={() => handleSend(q)}>
                {q}
              </Button>
            ))}
          </div>
        )}
        <div className="flex-1 overflow-y-auto space-y-3 mb-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[80%] px-3 py-2 rounded-lg text-sm ${
                  msg.role === "user" ? "bg-sky-500 text-white" : "bg-gray-100 text-gray-800"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {qa.isPending && (
            <div className="flex justify-start">
              <div className="bg-gray-100 px-3 py-2 rounded-lg text-sm text-gray-400">Thinking...</div>
            </div>
          )}
        </div>
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your health data..."
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <Button onClick={() => handleSend()} disabled={qa.isPending}>
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
