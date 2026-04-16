"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Switch, Spinner } from "@/components/ui";
import { Bell, Trash2, Edit2 } from "lucide-react";

interface PriceAlert {
  id: string;
  productName: string;
  targetPrice: number;
  currentPrice: number;
  isActive: boolean;
  createdAt: string;
  lastNotified?: string;
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<PriceAlert[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setAlerts([
      {
        id: "1",
        productName: "iPhone 15 Pro",
        targetPrice: 899,
        currentPrice: 999,
        isActive: true,
        createdAt: new Date().toISOString(),
        lastNotified: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: "2",
        productName: "Sony WH-1000XM5",
        targetPrice: 299,
        currentPrice: 399,
        isActive: true,
        createdAt: new Date().toISOString(),
      },
    ]);
    setIsLoading(false);
  }, []);

  if (isLoading) return <Spinner size="lg" />;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Bell size={32} />
          Price Alerts
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Get notified when prices drop
        </p>
      </div>

      <div className="space-y-4">
        {alerts.length === 0 ? (
          <Card className="p-12 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              No active alerts. Create one to get started!
            </p>
            <Button className="mt-4">Create New Alert</Button>
          </Card>
        ) : (
          alerts.map((alert) => (
            <Card key={alert.id} className="p-6">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {alert.productName}
                  </h3>
                  <div className="flex gap-6 mt-3 text-sm">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">
                        Current Price
                      </p>
                      <p className="font-bold text-blue-600">
                        ${alert.currentPrice.toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">
                        Target Price
                      </p>
                      <p className="font-bold text-green-600">
                        ${alert.targetPrice.toFixed(2)}
                      </p>
                    </div>
                    {alert.lastNotified && (
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">
                          Last Notified
                        </p>
                        <p className="font-bold">24 hours ago</p>
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex flex-col items-end gap-2">
                    <Switch checked={alert.isActive} />
                    <span className="text-xs text-gray-500">
                      {alert.isActive ? "Active" : "Inactive"}
                    </span>
                  </div>

                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      <Edit2 size={16} />
                    </Button>
                    <Button size="sm" variant="danger">
                      <Trash2 size={16} />
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>

      {alerts.length > 0 && (
        <Button className="mt-8 w-full md:w-auto">
          <Bell size={16} className="mr-2" />
          Create New Alert
        </Button>
      )}
    </div>
  );
}
