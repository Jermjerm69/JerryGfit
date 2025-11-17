"use client";

import { useQuery } from "@tanstack/react-query";
import { KPICard } from "@/components/dashboard/kpi-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { analyticsAPI, tasksAPI, projectsAPI } from "@/lib/api";
import {
  FolderOpen,
  CheckCircle,
  AlertTriangle,
  Users,
  TrendingUp,
  Clock,
  Loader2,
} from "lucide-react";

export default function DashboardPage() {
  // Fetch analytics data
  const { data: analytics, isLoading: analyticsLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: analyticsAPI.getDashboard,
  });

  // Fetch recent tasks
  const { data: tasks = [], isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => tasksAPI.getAll(0, 5),
  });

  // Fetch real projects from API
  const { data: projects = [] } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectsAPI.getAll(0, 10),
  });

  const recentTasks = tasks.slice(0, 5);
  const activeProjects = projects.filter((p) => p.status === "active");

  // Calculate high risks from risk_distribution
  const highRisks = (analytics?.risk_distribution?.high || 0) + (analytics?.risk_distribution?.critical || 0);

  if (analyticsLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back! Here&apos;s what&apos;s happening with your projects.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title="Total Tasks"
          value={analytics?.totals.total_tasks || 0}
          description="All tasks in the system"
          icon={FolderOpen}
          trend={{ value: 12, isPositive: true }}
        />
        <KPICard
          title="Completed Tasks"
          value={analytics?.totals.completed_tasks || 0}
          description="Tasks finished"
          icon={CheckCircle}
          trend={{ value: 8, isPositive: true }}
        />
        <KPICard
          title="High Risk Items"
          value={highRisks}
          description="Requires immediate attention"
          icon={AlertTriangle}
          trend={{ value: highRisks ? -15 : 0, isPositive: false }}
        />
        <KPICard
          title="Total Risks"
          value={analytics?.totals.total_risks || 0}
          description="All risks in the system"
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
            {activeProjects.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">
                No active projects. Create your first project to get started!
              </p>
            ) : (
              activeProjects.map((project) => (
                <div key={project.id} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">{project.name}</h4>
                    <span className="text-sm text-muted-foreground">
                      {project.progress}%
                    </span>
                  </div>
                  <Progress value={project.progress} />
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>
                      {project.due_date
                        ? `Due: ${new Date(project.due_date).toLocaleDateString()}`
                        : 'No due date'
                      }
                    </span>
                    <span className="text-xs text-muted-foreground capitalize">
                      {project.status}
                    </span>
                  </div>
                </div>
              ))
            )}
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
            {tasksLoading ? (
              <div className="flex justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
            ) : recentTasks.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">
                No tasks yet. Create your first task to get started!
              </p>
            ) : (
              recentTasks.map((task) => (
                <div key={task.id} className="flex items-center gap-3">
                  <div
                    className={`h-2 w-2 rounded-full ${
                      task.status === "done"
                        ? "bg-green-500"
                        : task.status === "in_progress"
                        ? "bg-yellow-500"
                        : "bg-gray-500"
                    }`}
                  />
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {task.title}
                    </p>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      {task.due_date && (
                        <>
                          <span>{new Date(task.due_date).toLocaleDateString()}</span>
                          <span>•</span>
                        </>
                      )}
                      <span className="capitalize">{task.status.toLowerCase().replace('_', ' ')}</span>
                    </div>
                  </div>
                  <span
                    className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                      task.priority === "HIGH" || task.priority === "URGENT"
                        ? "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
                        : task.priority === "MEDIUM"
                        ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400"
                        : "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
                    }`}
                  >
                    {task.priority.toLowerCase()}
                  </span>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}