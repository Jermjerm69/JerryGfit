"use client";

import { KPICard } from "@/components/dashboard/kpi-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { mockKPIData, mockProjects, mockTasks } from "@/data/mock-data";
import {
  FolderOpen,
  CheckCircle,
  AlertTriangle,
  Users,
  TrendingUp,
  Clock,
} from "lucide-react";

export default function DashboardPage() {
  const recentTasks = mockTasks.slice(0, 5);
  const activeProjects = mockProjects.filter((p) => p.status === "active");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back! Here's what's happening with your projects.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title="Total Projects"
          value={mockKPIData.totalProjects}
          description="Active and completed projects"
          icon={FolderOpen}
          trend={{ value: 12, isPositive: true }}
        />
        <KPICard
          title="Completed Tasks"
          value={mockKPIData.completedTasks}
          description="Tasks finished this month"
          icon={CheckCircle}
          trend={{ value: 8, isPositive: true }}
        />
        <KPICard
          title="High Risk Items"
          value={mockKPIData.highRisks}
          description="Requires immediate attention"
          icon={AlertTriangle}
          trend={{ value: -15, isPositive: false }}
        />
        <KPICard
          title="Active Users"
          value={mockKPIData.activeUsers}
          description={`of ${mockKPIData.totalUsers} total users`}
          icon={Users}
          trend={{ value: 5, isPositive: true }}
        />
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Active Projects
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {activeProjects.map((project) => (
              <div key={project.id} className="space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">{project.name}</h4>
                  <span className="text-sm text-muted-foreground">
                    {project.progress}%
                  </span>
                </div>
                <Progress value={project.progress} />
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>Due: {project.dueDate}</span>
                  <span>{project.team.length} members</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Recent Tasks
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentTasks.map((task) => (
              <div key={task.id} className="flex items-center gap-3">
                <div
                  className={`h-2 w-2 rounded-full ${
                    task.status === "done"
                      ? "bg-green-500"
                      : task.status === "in-progress"
                      ? "bg-yellow-500"
                      : "bg-gray-500"
                  }`}
                />
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium leading-none">
                    {task.title}
                  </p>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{task.assignee}</span>
                    <span>•</span>
                    <span>{task.dueDate}</span>
                  </div>
                </div>
                <span
                  className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                    task.priority === "high"
                      ? "bg-red-100 text-red-800"
                      : task.priority === "medium"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-green-100 text-green-800"
                  }`}
                >
                  {task.priority}
                </span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}