import { Sidebar } from "@/components/layout/sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen bg-background dark:bg-gradient-to-br dark:from-slate-900 dark:via-purple-900/10 dark:to-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6 bg-gradient-to-br from-blue-50/30 via-white to-purple-50/30 dark:from-transparent dark:via-transparent dark:to-transparent">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}