"use client";

import { useState } from "react";
import { Card, Button, Badge } from "@/components/ui";
import { BarChart3, Users, ShoppingCart, TrendingUp } from "lucide-react";

export default function AdminDashboardPage() {
  const [stats] = useState({
    totalUsers: 15234,
    totalOrders: 8934,
    totalRevenue: 456789.5,
    growth: 23.5,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Admin Dashboard
      </h1>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-4 mb-12">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Total Users
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                {stats.totalUsers.toLocaleString()}
              </p>
            </div>
            <Users size={32} className="text-blue-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Total Orders
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                {stats.totalOrders.toLocaleString()}
              </p>
            </div>
            <ShoppingCart size={32} className="text-green-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Revenue</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                ${(stats.totalRevenue / 1000).toFixed(0)}K
              </p>
            </div>
            <TrendingUp size={32} className="text-purple-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Growth</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
                +{stats.growth}%
              </p>
            </div>
            <BarChart3 size={32} className="text-yellow-600" />
          </div>
        </Card>
      </div>

      {/* Admin Actions */}
      <div className="grid gap-6 lg:grid-cols-2 mb-12">
        <Card className="p-6">
          <h2 className="font-bold text-gray-900 dark:text-white mb-4">
            System Management
          </h2>
          <div className="space-y-3">
            <Button className="w-full justify-start" variant="outline">
              Manage Users
            </Button>
            <Button className="w-full justify-start" variant="outline">
              View Reports
            </Button>
            <Button className="w-full justify-start" variant="outline">
              System Settings
            </Button>
            <Button className="w-full justify-start" variant="outline">
              Database Backup
            </Button>
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="font-bold text-gray-900 dark:text-white mb-4">
            Content Management
          </h2>
          <div className="space-y-3">
            <Button className="w-full justify-start" variant="outline">
              Manage Products
            </Button>
            <Button className="w-full justify-start" variant="outline">
              Manage Categories
            </Button>
            <Button className="w-full justify-start" variant="outline">
              Content Flags
            </Button>
            <Button className="w-full justify-start" variant="outline">
              Analytics
            </Button>
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="p-6">
        <h2 className="font-bold text-gray-900 dark:text-white mb-4">
          Recent Activity
        </h2>
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="flex items-center justify-between p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
            >
              <div>
                <p className="font-semibold text-gray-900 dark:text-white">
                  User #{(1000 + i).toLocaleString()} created new order
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Just now
                </p>
              </div>
              <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                New Order
              </Badge>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
