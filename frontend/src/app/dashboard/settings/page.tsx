"use client";
import ProviderStatus from "@/components/ProviderStatus";
import ProviderSettings from "@/components/ProviderSettings";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { updateProfile } from "@/lib/auth";

export default function SettingsPage() {
  const { user, fetchUser } = useAuth();
  const [name, setName] = useState(user?.full_name || "");
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    await updateProfile({ full_name: name });
    await fetchUser();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-bold text-gray-900">Settings</h1>

      <Card>
        <CardHeader><CardTitle>Profile</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div>
            <Label>Name</Label>
            <Input value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div>
            <Label>Email</Label>
            <Input value={user?.email || ""} disabled />
          </div>
          {saved && <p className="text-emerald-500 text-sm">✓ Saved</p>}
          <Button onClick={handleSave} className="bg-sky-500 hover:bg-sky-600">Save Profile</Button>
        </CardContent>
      </Card>

      <ProviderStatus />
      <ProviderSettings />
    </div>
  );
}
