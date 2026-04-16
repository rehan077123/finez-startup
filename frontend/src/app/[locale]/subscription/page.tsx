"use client";

import { useState } from "react";
import { Card, Button, Badge, Switch } from "@/components/ui";
import { CreditCard, Check, X } from "lucide-react";

interface Plan {
  id: string;
  name: string;
  price: number;
  features: string[];
  current: boolean;
}

export default function SubscriptionPage() {
  const [plans] = useState<Plan[]>([
    {
      id: "free",
      name: "Free",
      price: 0,
      current: true,
      features: [
        "Basic search",
        "Price tracking (up to 5 alerts)",
        "Limited comparisons",
      ],
    },
    {
      id: "pro",
      name: "FineZ Pro",
      price: 9.99,
      current: false,
      features: [
        "Advanced search",
        "Unlimited price alerts",
        "Unlimited comparisons",
        "Priority support",
        "Exclusive deals",
      ],
    },
    {
      id: "premium",
      name: "FineZ Premium",
      price: 19.99,
      current: false,
      features: [
        "Everything in Pro",
        "AI-powered recommendations",
        "Custom guides",
        "Premium analytics",
        "API access",
      ],
    },
  ]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Subscription Plans
      </h1>
      <p className="text-gray-600 dark:text-gray-400 mb-12">
        Choose the perfect plan for your needs
      </p>

      <div className="grid gap-8 md:grid-cols-3 mb-12">
        {plans.map((plan) => (
          <Card
            key={plan.id}
            className={`p-8 ${plan.current ? "ring-2 ring-blue-500" : ""}`}
          >
            {plan.current && (
              <Badge className="mb-4 bg-blue-600">Current Plan</Badge>
            )}

            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {plan.name}
            </h2>
            <p className="text-3xl font-bold text-blue-600 mb-6">
              ${plan.price}
              <span className="text-lg text-gray-600 dark:text-gray-400 font-normal">
                /month
              </span>
            </p>

            <Button
              className="w-full mb-8"
              variant={plan.current ? "outline" : "primary"}
            >
              {plan.current ? "Current Plan" : "Upgrade"}
            </Button>

            <div className="space-y-3">
              {plan.features.map((feature, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <Check size={16} className="text-green-600" />
                  <span className="text-gray-700 dark:text-gray-300">
                    {feature}
                  </span>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>

      {/* Billing History */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
          Billing History
        </h2>
        <div className="space-y-4">
          {[
            { date: "Jan 15, 2024", amount: 0, status: "Free Plan" },
            { date: "Dec 15, 2023", amount: 0, status: "Free Plan" },
          ].map((bill, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
            >
              <div>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {bill.date}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {bill.status}
                </p>
              </div>
              <p className="font-bold text-gray-900 dark:text-white">
                ${bill.amount.toFixed(2)}
              </p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
