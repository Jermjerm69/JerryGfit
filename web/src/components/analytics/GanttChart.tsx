'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock } from 'lucide-react';
import { useMemo } from 'react';

interface Task {
  id: number;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'done' | 'blocked';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date: string | null;
  created_at: string;
}

interface GanttChartProps {
  tasks: Task[];
}

export function GanttChart({ tasks }: GanttChartProps) {
  // Calculate date range for the chart
  const dateRange = useMemo(() => {
    if (tasks.length === 0) {
      const today = new Date();
      const futureDate = new Date();
      futureDate.setDate(today.getDate() + 30);
      return { start: today, end: futureDate, days: 30 };
    }

    const dates = tasks
      .filter(t => t.due_date)
      .map(t => new Date(t.due_date!));

    const createdDates = tasks.map(t => new Date(t.created_at));

    const allDates = [...dates, ...createdDates];
    const start = new Date(Math.min(...allDates.map(d => d.getTime())));
    const end = new Date(Math.max(...allDates.map(d => d.getTime())));

    // Add buffer
    start.setDate(start.getDate() - 2);
    end.setDate(end.getDate() + 7);

    const days = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));

    return { start, end, days: Math.max(days, 14) };
  }, [tasks]);

  // Generate week headers
  const weeks = useMemo(() => {
    const result = [];
    const current = new Date(dateRange.start);
    let weekCount = 0;

    while (current <= dateRange.end) {
      const weekStart = new Date(current);
      const weekEnd = new Date(current);
      weekEnd.setDate(weekEnd.getDate() + 6);

      result.push({
        id: weekCount++,
        start: weekStart,
        end: weekEnd > dateRange.end ? dateRange.end : weekEnd,
        label: `Week ${weekCount}`,
        days: Math.min(7, Math.ceil((dateRange.end.getTime() - current.getTime()) / (1000 * 60 * 60 * 24)))
      });

      current.setDate(current.getDate() + 7);
    }

    return result;
  }, [dateRange]);

  // Calculate task bar position and width
  const getTaskBar = (task: Task) => {
    const startDate = new Date(task.created_at);
    const endDate = task.due_date ? new Date(task.due_date) : new Date();

    if (!task.due_date) {
      endDate.setDate(startDate.getDate() + 7); // Default 1 week duration
    }

    const totalDuration = dateRange.end.getTime() - dateRange.start.getTime();
    const taskStart = startDate.getTime() - dateRange.start.getTime();
    const taskDuration = endDate.getTime() - startDate.getTime();

    const left = Math.max(0, (taskStart / totalDuration) * 100);
    const width = Math.min(100 - left, (taskDuration / totalDuration) * 100);

    return { left: `${left}%`, width: `${width}%` };
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done':
        return 'bg-green-500';
      case 'in_progress':
        return 'bg-blue-500';
      case 'blocked':
        return 'bg-red-500';
      default:
        return 'bg-gray-400';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'border-red-500';
      case 'high':
        return 'border-orange-500';
      case 'medium':
        return 'border-yellow-500';
      default:
        return 'border-gray-400';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'done':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'blocked':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800/50 dark:text-gray-300';
    }
  };

  if (tasks.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Gantt Chart
          </CardTitle>
          <CardDescription>Project timeline and task dependencies</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12 text-muted-foreground">
            <Calendar className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No tasks to display. Create tasks to see your project timeline.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Calendar className="h-5 w-5" />
          Gantt Chart
        </CardTitle>
        <CardDescription>
          Project timeline visualization • {tasks.length} tasks • {dateRange.days} days
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Legend */}
          <div className="flex items-center gap-4 text-xs text-muted-foreground pb-2 border-b">
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded bg-gray-400" />
              <span>To Do</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded bg-blue-500" />
              <span>In Progress</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded bg-green-500" />
              <span>Done</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded bg-red-500" />
              <span>Blocked</span>
            </div>
          </div>

          {/* Gantt Chart Container */}
          <div className="overflow-x-auto">
            <div className="min-w-[800px]">
              {/* Timeline Header */}
              <div className="flex border-b">
                <div className="w-64 flex-shrink-0 px-4 py-2 font-medium text-sm border-r bg-muted/50">
                  Task Name
                </div>
                <div className="flex-1 flex">
                  {weeks.map((week) => (
                    <div
                      key={week.id}
                      className="flex-1 px-2 py-2 text-xs text-center border-r bg-muted/50 font-medium"
                    >
                      {week.label}
                      <div className="text-muted-foreground">
                        {week.start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Task Rows */}
              <div className="relative">
                {tasks.map((task, index) => {
                  const barPosition = getTaskBar(task);

                  return (
                    <div
                      key={task.id}
                      className={`flex border-b hover:bg-muted/30 transition-colors ${
                        index % 2 === 0 ? 'bg-background' : 'bg-muted/5'
                      }`}
                    >
                      {/* Task Name Column */}
                      <div className="w-64 flex-shrink-0 px-4 py-3 border-r">
                        <div className="space-y-1">
                          <div className="font-medium text-sm line-clamp-1" title={task.title}>
                            {task.title}
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge className={getStatusBadge(task.status)} variant="outline">
                              {task.status.replace('_', ' ')}
                            </Badge>
                            {task.due_date && (
                              <span className="text-xs text-muted-foreground flex items-center gap-1">
                                <Clock className="h-3 w-3" />
                                {new Date(task.due_date).toLocaleDateString('en-US', {
                                  month: 'short',
                                  day: 'numeric'
                                })}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Timeline Column */}
                      <div className="flex-1 relative py-3 px-2">
                        {/* Week Grid Lines */}
                        <div className="absolute inset-0 flex">
                          {weeks.map((week, i) => (
                            <div
                              key={week.id}
                              className={`flex-1 ${
                                i < weeks.length - 1 ? 'border-r border-muted' : ''
                              }`}
                            />
                          ))}
                        </div>

                        {/* Task Bar */}
                        <div className="relative h-8">
                          <div
                            className={`absolute h-8 rounded-md ${getStatusColor(
                              task.status
                            )} ${getPriorityColor(
                              task.priority
                            )} border-l-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer flex items-center px-2`}
                            style={{
                              left: barPosition.left,
                              width: barPosition.width,
                              minWidth: '40px',
                            }}
                            title={`${task.title}\nStart: ${new Date(task.created_at).toLocaleDateString()}\nDue: ${
                              task.due_date
                                ? new Date(task.due_date).toLocaleDateString()
                                : 'Not set'
                            }\nPriority: ${task.priority}`}
                          >
                            <span className="text-xs text-white font-medium truncate">
                              {task.status === 'done' ? '✓ ' : ''}
                              {parseFloat(barPosition.width) > 15 ? task.title : ''}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Today Marker */}
              <div className="relative h-0">
                {(() => {
                  const today = new Date();
                  if (today >= dateRange.start && today <= dateRange.end) {
                    const totalDuration = dateRange.end.getTime() - dateRange.start.getTime();
                    const todayPosition = today.getTime() - dateRange.start.getTime();
                    const left = (todayPosition / totalDuration) * 100;

                    return (
                      <div
                        className="absolute top-0 bottom-0 w-0.5 bg-blue-600 z-10"
                        style={{ left: `calc(16rem + ${left}%)` }}
                      >
                        <div className="absolute -top-8 -left-8 bg-blue-600 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                          Today
                        </div>
                      </div>
                    );
                  }
                  return null;
                })()}
              </div>
            </div>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-4 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-muted-foreground">
                {tasks.filter(t => t.status === 'todo').length}
              </div>
              <div className="text-xs text-muted-foreground">To Do</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {tasks.filter(t => t.status === 'in_progress').length}
              </div>
              <div className="text-xs text-muted-foreground">In Progress</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {tasks.filter(t => t.status === 'done').length}
              </div>
              <div className="text-xs text-muted-foreground">Completed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {tasks.filter(t => t.status === 'blocked').length}
              </div>
              <div className="text-xs text-muted-foreground">Blocked</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
