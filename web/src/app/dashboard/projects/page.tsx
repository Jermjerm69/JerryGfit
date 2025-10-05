"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { mockRisks, mockTasks } from "@/data/mock-data";
import {
  AlertTriangle,
  CheckCircle,
  Plus,
  Filter,
  Download,
  Calendar,
} from "lucide-react";

export default function ProjectsPage() {
  const [activeTab, setActiveTab] = useState("risks");

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "high":
        return "bg-red-100 text-red-800 border-red-200";
      case "medium":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "low":
        return "bg-green-100 text-green-800 border-green-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "done":
      case "completed":
      case "resolved":
        return "bg-green-100 text-green-800 border-green-200";
      case "in-progress":
      case "in progress":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "todo":
      case "open":
        return "bg-gray-100 text-gray-800 border-gray-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Project Management</h1>
          <p className="text-muted-foreground">
            Manage risks, tasks, and track project progress
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            Filter
          </Button>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Add New
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger
            value="risks"
            isActive={activeTab === "risks"}
            onClick={() => setActiveTab("risks")}
          >
            <AlertTriangle className="h-4 w-4 mr-2" />
            Risk Register
          </TabsTrigger>
          <TabsTrigger
            value="tasks"
            isActive={activeTab === "tasks"}
            onClick={() => setActiveTab("tasks")}
          >
            <CheckCircle className="h-4 w-4 mr-2" />
            Tasks
          </TabsTrigger>
          <TabsTrigger
            value="burndown"
            isActive={activeTab === "burndown"}
            onClick={() => setActiveTab("burndown")}
          >
            <Calendar className="h-4 w-4 mr-2" />
            Burndown
          </TabsTrigger>
        </TabsList>

        <TabsContent value="risks" activeValue={activeTab}>
          <Card>
            <CardHeader>
              <CardTitle>Risk Register</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockRisks.map((risk) => (
                  <div
                    key={risk.id}
                    className="border rounded-lg p-4 space-y-3 hover:bg-muted/30 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-medium">{risk.title}</h3>
                          <Badge className={getSeverityColor(risk.severity)}>
                            {risk.severity}
                          </Badge>
                          <Badge className={getStatusColor(risk.status)}>
                            {risk.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {risk.description}
                        </p>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {risk.id}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Probability:</span>
                        <p className="font-medium">{risk.probability}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Impact:</span>
                        <p className="font-medium">{risk.impact}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Owner:</span>
                        <p className="font-medium">{risk.owner}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Created:</span>
                        <p className="font-medium">{risk.createdDate}</p>
                      </div>
                    </div>

                    <div>
                      <span className="text-sm text-muted-foreground">
                        Mitigation Plan:
                      </span>
                      <p className="text-sm mt-1">{risk.mitigationPlan}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tasks" activeValue={activeTab}>
          <div className="grid gap-6 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-gray-500" />
                  To Do ({mockTasks.filter((t) => t.status === "todo").length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {mockTasks
                  .filter((task) => task.status === "todo")
                  .map((task) => (
                    <div key={task.id} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-start justify-between">
                        <h4 className="font-medium text-sm">{task.title}</h4>
                        <Badge className={getSeverityColor(task.priority)}>
                          {task.priority}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {task.description}
                      </p>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span>{task.assignee}</span>
                        <span>{task.dueDate}</span>
                      </div>
                    </div>
                  ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-blue-500" />
                  In Progress (
                  {mockTasks.filter((t) => t.status === "in-progress").length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {mockTasks
                  .filter((task) => task.status === "in-progress")
                  .map((task) => (
                    <div key={task.id} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-start justify-between">
                        <h4 className="font-medium text-sm">{task.title}</h4>
                        <Badge className={getSeverityColor(task.priority)}>
                          {task.priority}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {task.description}
                      </p>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span>{task.assignee}</span>
                        <span>{task.dueDate}</span>
                      </div>
                    </div>
                  ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-green-500" />
                  Done ({mockTasks.filter((t) => t.status === "done").length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {mockTasks
                  .filter((task) => task.status === "done")
                  .map((task) => (
                    <div key={task.id} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-start justify-between">
                        <h4 className="font-medium text-sm">{task.title}</h4>
                        <Badge className={getSeverityColor(task.priority)}>
                          {task.priority}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {task.description}
                      </p>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span>{task.assignee}</span>
                        <span>{task.dueDate}</span>
                      </div>
                    </div>
                  ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="burndown" activeValue={activeTab}>
          <Card>
            <CardHeader>
              <CardTitle>Burndown Chart</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80 flex items-center justify-center border-2 border-dashed border-muted-foreground/25 rounded-lg">
                <div className="text-center space-y-2">
                  <Calendar className="h-12 w-12 mx-auto text-muted-foreground" />
                  <h3 className="text-lg font-medium">Burndown Chart Placeholder</h3>
                  <p className="text-sm text-muted-foreground max-w-sm">
                    This section would contain an interactive burndown chart showing
                    task completion progress over time. Integration with chart
                    libraries like Chart.js or Recharts would be implemented here.
                  </p>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">45</div>
                  <div className="text-sm text-muted-foreground">
                    Remaining Tasks
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">67%</div>
                  <div className="text-sm text-muted-foreground">
                    Sprint Progress
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">3</div>
                  <div className="text-sm text-muted-foreground">Days Left</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}