"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "@/components/theme-toggle";
import {
  LayoutDashboard,
  Bot,
  FolderKanban,
  BarChart3,
  Settings,
  User,
  LogOut,
  Dumbbell,
} from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "AI Studio",
    href: "/dashboard/ai-studio",
    icon: Bot,
  },
  {
    name: "Projects",
    href: "/dashboard/projects",
    icon: FolderKanban,
  },
  {
    name: "Analytics",
    href: "/dashboard/analytics",
    icon: BarChart3,
  },
  {
    name: "Settings",
    href: "/dashboard/settings",
    icon: Settings,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-64 flex-col bg-card/50 backdrop-blur-sm border-r border-border/50 dark:bg-card/30">
      <div className="flex h-16 items-center justify-between px-6 border-b border-border/50">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
            <Dumbbell className="h-5 w-5 text-white" />
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
            JerryGFit
          </h1>
        </div>
        <ThemeToggle />
      </div>

      {/* Coach Image Section */}
      <div className="p-4 mx-4 mt-4 rounded-lg bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-950/30 dark:to-purple-950/30 border border-border/50">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold text-lg">
            🏋️
          </div>
          <div>
            <p className="text-sm font-medium">JerryGFit AI Coach</p>
            <p className="text-xs text-muted-foreground">Ready to help!</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-4 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href || (pathname.startsWith(item.href) && item.href !== "/dashboard");
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all duration-200 hover:scale-[1.02]",
                isActive
                  ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/25"
                  : "text-muted-foreground hover:bg-accent/80 hover:text-accent-foreground"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-border/50 p-4">
        <div className="flex items-center gap-3 rounded-lg px-3 py-2 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800/50 dark:to-gray-900/50">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            <User className="h-4 w-4" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">Jerry Coach</p>
            <p className="text-xs text-muted-foreground">coach@jerryfit.com</p>
          </div>
        </div>
        <button className="mt-2 flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent/80 hover:text-accent-foreground transition-colors">
          <LogOut className="h-4 w-4" />
          Sign out
        </button>
      </div>
    </div>
  );
}