"use client";

import { useState } from "react";
import { Card, Button, Input, Spinner } from "@/components/ui";
import { CheckCircle, AlertCircle } from "lucide-react";

export default function VerifyEmailPage() {
  const [code, setCode] = useState("");
  const [status, setStatus] = useState<"pending" | "success" | "error" | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(false);

  const handleVerify = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/verify-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: code }),
      });

      if (res.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <Card className="w-full max-w-md p-8">
        {status === "success" ? (
          <div className="text-center">
            <CheckCircle size={64} className="mx-auto text-green-600 mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Email Verified!
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Your email has been verified successfully.
            </p>
            <Button className="w-full">Go to Dashboard</Button>
          </div>
        ) : status === "error" ? (
          <div className="text-center">
            <AlertCircle size={64} className="mx-auto text-red-600 mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Verification Failed
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              The verification code is invalid or has expired.
            </p>
            <Button
              className="w-full mb-2"
              variant="outline"
              onClick={() => {
                setStatus(null);
                setCode("");
              }}
            >
              Try Again
            </Button>
          </div>
        ) : (
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Verify Your Email
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Enter the verification code sent to your email.
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                  Verification Code
                </label>
                <Input
                  placeholder="Enter 6-digit code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                />
              </div>

              <Button
                className="w-full"
                onClick={handleVerify}
                disabled={isLoading || code.length < 6}
              >
                {isLoading ? <Spinner size="sm" /> : "Verify"}
              </Button>

              <Button className="w-full" variant="outline">
                Resend Code
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
