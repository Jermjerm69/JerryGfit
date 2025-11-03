'use client';

import { useEffect } from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-purple-900/10 dark:to-slate-900">
      <div className="text-center space-y-6 p-8 max-w-lg">
        <AlertTriangle className="h-24 w-24 mx-auto text-red-500" />
        <h1 className="text-4xl font-bold">Something went wrong!</h1>
        <p className="text-lg text-muted-foreground">
          An error occurred while processing your request. Please try again.
        </p>
        {error.message && (
          <div className="bg-muted p-4 rounded-lg text-sm text-left">
            <p className="font-medium mb-1">Error details:</p>
            <code className="text-xs">{error.message}</code>
          </div>
        )}
        <div className="flex gap-4 justify-center">
          <Button onClick={reset}>Try Again</Button>
          <Button variant="outline" onClick={() => window.location.href = '/dashboard'}>
            Go to Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}
