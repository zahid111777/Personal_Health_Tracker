"use client";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import RoleGuard from "@/components/RoleGuard";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <RoleGuard>
      <div className="min-h-screen bg-[#F0F9FF]">
        <Navbar />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-6 ml-56 mt-16">{children}</main>
        </div>
      </div>
    </RoleGuard>
  );
}
