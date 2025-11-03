'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingDown } from 'lucide-react';

interface BurndownDataPoint {
  date: string;
  remaining_tasks: number;
  completed_tasks: number;
}

interface BurndownChartProps {
  data: BurndownDataPoint[];
}

export function BurndownChart({ data }: BurndownChartProps) {
  // Format data for display
  const formattedData = data.map(point => ({
    date: new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    remaining: point.remaining_tasks,
    completed: point.completed_tasks,
    total: point.remaining_tasks + point.completed_tasks,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingDown className="h-5 w-5" />
          Burndown Chart
        </CardTitle>
        <CardDescription>Task completion progress over time</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={formattedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              className="text-xs text-muted-foreground"
              tick={{ fill: 'currentColor' }}
            />
            <YAxis
              className="text-xs text-muted-foreground"
              tick={{ fill: 'currentColor' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--background))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '6px',
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="remaining"
              stroke="#ef4444"
              strokeWidth={2}
              name="Remaining Tasks"
              dot={{ fill: '#ef4444', r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="completed"
              stroke="#22c55e"
              strokeWidth={2}
              name="Completed Tasks"
              dot={{ fill: '#22c55e', r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
