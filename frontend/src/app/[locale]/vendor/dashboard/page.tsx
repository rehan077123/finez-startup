"use client";

import { useState } from "react";
import { Card, Button, Badge, Spinner, Input } from "@/components/ui";
import { LineChart, Package, DollarSign, TrendingUp } from "lucide-react";

export default function VendorDashboardPage() {
  const [stats] = useState({
    totalSales: 24850.5,
    ordersCount: 328,
    productCount: 45,
    rating: 4.8,
    growth: 12.5,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Vendor Dashboard
      </h1>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-4 mb-12">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Total Sales
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                ${stats.totalSales.toFixed(2)}
              </p>
            </div>
            <DollarSign size={32} className="text-green-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Orders
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                {stats.ordersCount}
              </p>
            </div>
            <Package size={32} className="text-blue-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Products</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                {stats.productCount}
              </p>
            </div>
            <LineChart size={32} className="text-purple-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Rating</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                ⭐ {stats.rating}
              </p>
            </div>
            <TrendingUp size={32} className="text-yellow-600" />
          </div>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2 p-6">
          <h2 className="font-bold text-gray-900 dark:text-white mb-4">
            Recent Orders
          </h2>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="flex items-center justify-between p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
              >
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    Order #FZ-2024-{String(i).padStart(3, "0")}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    $149.99
                  </p>
                </div>
                <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                  Pending
                </Badge>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="font-bold text-gray-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <div className="space-y-3">
            <Button className="w-full">Add Product</Button>
            <Button className="w-full" variant="outline">Manage Inventory</Button>
            <Button className="w-full" variant="outline">View Analytics</Button>
            <Button className="w-full" variant="outline">Settings</Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
