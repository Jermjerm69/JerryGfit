"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { analyticsAPI, tasksAPI } from "@/lib/api";
import { BurndownChart } from "@/components/analytics/BurndownChart";
import { TaskDistributionChart } from "@/components/analytics/TaskDistributionChart";
import { VelocityChart } from "@/components/analytics/VelocityChart";
import { toast } from "@/components/providers/toast-provider";
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Download,
  RefreshCw,
  Calendar,
  PieChart,
  Activity,
  Loader2,
  FileText,
  FileSpreadsheet,
} from "lucide-react";

export default function AnalyticsPage() {
  // Fetch analytics data
  const { data: analytics, isLoading: analyticsLoading, refetch } = useQuery({
    queryKey: ['analytics'],
    queryFn: analyticsAPI.getDashboard,
  });

  // Fetch all tasks for distribution calculation
  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks-all'],
    queryFn: () => tasksAPI.getAll(0, 1000),
  });

  if (analyticsLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  // Calculate task distribution
  const taskDistribution = [
    {
      name: 'To Do',
      value: tasks.filter(t => t.status === 'todo').length,
      color: '#94a3b8',
    },
    {
      name: 'In Progress',
      value: tasks.filter(t => t.status === 'in_progress').length,
      color: '#3b82f6',
    },
    {
      name: 'Completed',
      value: tasks.filter(t => t.status === 'done').length,
      color: '#22c55e',
    },
    {
      name: 'Blocked',
      value: tasks.filter(t => t.status === 'blocked').length,
      color: '#ef4444',
    },
  ];

  // Use velocity data from backend
  const velocityData = analytics?.velocity_data?.map(item => ({
    week: item.week,
    tasksCompleted: item.tasks_completed,
    average: item.average
  })) || [];

  // Get metrics from backend
  const completionRate = analytics?.totals.completion_rate || 0;
  const velocity = analytics?.totals.velocity || 0;
  const avgLeadTime = analytics?.totals.average_lead_time || 0;
  const riskScore = analytics?.totals.risk_score || 0;

  // Use real risk distribution from backend
  const riskDistributionData = analytics?.risk_distribution ? [
    { name: 'Low', value: analytics.risk_distribution.low, color: '#22c55e' },
    { name: 'Medium', value: analytics.risk_distribution.medium, color: '#eab308' },
    { name: 'High', value: analytics.risk_distribution.high, color: '#f97316' },
    { name: 'Critical', value: analytics.risk_distribution.critical, color: '#ef4444' },
  ] : [];

  const totalRisks = riskDistributionData.reduce((sum, risk) => sum + risk.value, 0);

  // Export functions
  const handleExportPDF = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/analytics/export/pdf`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error('Failed to export PDF');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analytics_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      toast.success('PDF report downloaded successfully!');
    } catch {
      toast.error('Failed to export PDF report');
    }
  };

  const handleExportExcel = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/analytics/export/excel`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error('Failed to export Excel');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analytics_report_${new Date().toISOString().split('T')[0]}.xlsx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      toast.success('Excel report downloaded successfully!');
    } catch {
      toast.error('Failed to export Excel report');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <BarChart3 className="h-8 w-8" />
            Analytics
          </h1>
          <p className="text-muted-foreground">
            Track project performance and team productivity
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => refetch()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Calendar className="h-4 w-4 mr-2" />
            Date Range
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export Report
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={handleExportPDF}>
                <FileText className="h-4 w-4 mr-2" />
                Export as PDF
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleExportExcel}>
                <FileSpreadsheet className="h-4 w-4 mr-2" />
                Export as Excel
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Project Velocity</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{velocity.toFixed(1)}</div>
            <p className="text-xs text-muted-foreground">
              tasks per week
            </p>
            <div className="flex items-center text-xs text-green-600 mt-1">
              <TrendingUp className="h-3 w-3 mr-1" />
              +12% from last month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completion Rate</CardTitle>
            <PieChart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completionRate}%</div>
            <p className="text-xs text-muted-foreground">
              tasks completed on time
            </p>
            <div className="flex items-center text-xs text-green-600 mt-1">
              <TrendingUp className="h-3 w-3 mr-1" />
              +5% from last month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Lead Time</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgLeadTime}</div>
            <p className="text-xs text-muted-foreground">
              days per task
            </p>
            <div className="flex items-center text-xs text-red-600 mt-1">
              <TrendingDown className="h-3 w-3 mr-1" />
              +0.3 days from last month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Risk Score</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{riskScore}</div>
            <p className="text-xs text-muted-foreground">
              total risk points
            </p>
            <div className="flex items-center text-xs text-green-600 mt-1">
              <TrendingDown className="h-3 w-3 mr-1" />
              -8% from last month
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Burndown Chart */}
        {analytics?.burndown && (
          <BurndownChart data={analytics.burndown.data_points || []} />
        )}

        {/* Task Distribution Chart */}
        <TaskDistributionChart data={taskDistribution} />
      </div>

      <div className="grid gap-6 md:grid-cols-1">
        {/* Velocity Chart */}
        <VelocityChart data={velocityData} />
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Risk Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Risk Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {riskDistributionData.map((risk) => (
                <div key={risk.name} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div
                        className="h-2 w-2 rounded-full"
                        style={{ backgroundColor: risk.color }}
                      />
                      <span className="text-sm font-medium">{risk.name} Risk</span>
                    </div>
                    <span className="text-sm text-muted-foreground">
                      {risk.value} items
                    </span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full transition-all duration-300"
                      style={{
                        backgroundColor: risk.color,
                        width: totalRisks > 0 ? `${(risk.value / totalRisks) * 100}%` : '0%',
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Team Performance Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Performance Metrics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 rounded-lg border">
                <div className="space-y-1">
                  <div className="font-medium">Task Completion Velocity</div>
                  <div className="text-sm text-muted-foreground">
                    Average tasks completed per week
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-600">{velocity.toFixed(1)}</div>
                  <div className="text-xs text-muted-foreground">tasks/week</div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border">
                <div className="space-y-1">
                  <div className="font-medium">Sprint Success Rate</div>
                  <div className="text-sm text-muted-foreground">
                    Percentage of sprints completed on time
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-blue-600">87%</div>
                  <div className="text-xs text-muted-foreground">success rate</div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border">
                <div className="space-y-1">
                  <div className="font-medium">Risk Mitigation Rate</div>
                  <div className="text-sm text-muted-foreground">
                    Risks successfully mitigated
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-purple-600">92%</div>
                  <div className="text-xs text-muted-foreground">mitigated</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
