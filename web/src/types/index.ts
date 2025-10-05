export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role: "admin" | "user" | "manager";
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  status: "active" | "completed" | "planning" | "on-hold";
  progress: number;
  startDate: string;
  dueDate: string;
  team: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in-progress" | "done";
  priority: "low" | "medium" | "high";
  assignee: string;
  project: string;
  dueDate: string;
  createdAt: string;
  updatedAt: string;
}

export interface Risk {
  id: string;
  title: string;
  description: string;
  severity: "Low" | "Medium" | "High" | "Critical";
  probability: "Low" | "Medium" | "High";
  impact: "Low" | "Medium" | "High";
  status: "Open" | "In Progress" | "Closed" | "Resolved";
  owner: string;
  project?: string;
  createdDate: string;
  updatedDate?: string;
  mitigationPlan: string;
}

export interface KPIData {
  totalProjects: number;
  activeProjects: number;
  completedTasks: number;
  totalRisks: number;
  highRisks: number;
  mediumRisks: number;
  lowRisks: number;
  totalUsers: number;
  activeUsers: number;
}

export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

export interface TimeSeriesData {
  month: string;
  active: number;
  completed: number;
}