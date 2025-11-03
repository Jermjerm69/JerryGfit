'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity } from 'lucide-react';

interface VelocityData {
  week: string;
  tasksCompleted: number;
  average: number;
}

interface VelocityChartProps {
  data: VelocityData[];
}

export function VelocityChart({ data }: VelocityChartProps) {
  const averageVelocity = data.reduce((sum, d) => sum + d.tasksCompleted, 0) / data.length;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5" />
          Team Velocity
        </CardTitle>
        <CardDescription>Tasks completed per week</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="week"
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
            <ReferenceLine
              y={averageVelocity}
              stroke="#6366f1"
              strokeDasharray="3 3"
              label={{ value: 'Average', position: 'right' }}
            />
            <Bar
              dataKey="tasksCompleted"
              fill="#10b981"
              name="Tasks Completed"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
        <div className="mt-4 text-center">
          <p className="text-sm text-muted-foreground">
            Average Velocity: <span className="font-medium text-foreground">{averageVelocity.toFixed(1)} tasks/week</span>
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
