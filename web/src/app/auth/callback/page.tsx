"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function AuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      // Get tokens from URL query parameters
      const accessToken = searchParams.get("access_token");
      const refreshToken = searchParams.get("refresh_token");
      const errorParam = searchParams.get("error");

      if (errorParam) {
        setError(decodeURIComponent(errorParam));
        // Redirect to login after 3 seconds
        setTimeout(() => {
          router.push("/auth/login");
        }, 3000);
        return;
      }

      if (accessToken && refreshToken) {
        // Store tokens in localStorage
        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);

        // Redirect to dashboard
        router.push("/dashboard");
      } else {
        setError("Authentication failed. No tokens received.");
        setTimeout(() => {
          router.push("/auth/login");
        }, 3000);
      }
    };

    handleCallback();
  }, [router, searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-purple-900/10 dark:to-slate-900">
      <div className="text-center space-y-4">
        {error ? (
          <>
            <div className="text-red-600 dark:text-red-400 text-xl font-semibold">
              {error}
            </div>
            <p className="text-muted-foreground">
              Redirecting to login page...
            </p>
          </>
        ) : (
          <>
            <Loader2 className="h-12 w-12 animate-spin mx-auto text-blue-600 dark:text-blue-400" />
            <div className="text-xl font-semibold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
              Completing sign in...
            </div>
          </>
        )}
      </div>
    </div>
  );
}
