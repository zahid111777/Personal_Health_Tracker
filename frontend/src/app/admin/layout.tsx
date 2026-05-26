"use client";
import RoleGuard from "@/components/RoleGuard";
import Navbar from "@/components/Navbar";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <RoleGuard requiredRole="admin">
      <div className="min-h-screen bg-[#F0F9FF]">
        <Navbar />
        <main className="p-6 mt-16 max-w-4xl mx-auto">{children}</main>
      </div>
    </RoleGuard>
  );
}
