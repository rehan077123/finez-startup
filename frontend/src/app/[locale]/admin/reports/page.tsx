"use client";

import { useState } from "react";
import { Card, Button, Badge, Select } from "@/components/ui";
import { BarChart3, LineChart, TrendingUp, Users } from "lucide-react";

interface ReportData {
  date: string;
  value: number;
  change: number;
}

export default function AdminReportsPage() {
  const [reportType, setReportType] = useState<"sales" | "users" | "products" | "performance">("sales");

  const mockData: Record<string, ReportData[]> = {
    sales: [
      { date: "Jan", value: 45000, change: 12 },
      { date: "Feb", value: 52000, change: 15 },
      { date: "Mar", value: 48000, change: -8 },
      { date: "Apr", value: 61000, change: 27 },
    ],
    users: [
      { date: "Jan", value: 2340, change: 5 },
      { date: "Feb", value: 2890, change: 23 },
      { date: "Mar", value: 3125, change: 8 },
      { date: "Apr", value: 3890, change: 24 },
    ],
  };

  const data = mockData[reportType] || mockData.sales;

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Reports & Analytics
        </h1>
        <Button>Export Report</Button>
      </div>

      {/* Report Type Selector */}
      <Card className="p-6 mb-8">
        <div className="grid gap-4 md:grid-cols-4">
          {[
            { id: "sales", label: "Sales", icon: TrendingUp },
            { id: "users", label: "Users", icon: Users },
            { id: "products", label: "Products", icon: BarChart3 },
            { id: "performance", label: "Performance", icon: LineChart },
          ].map((report) => (
            <button
              key={report.id}
              onClick={() => setReportType(report.id as any)}
              className={`p-4 rounded-lg border-2 transition-all ${
                reportType === report.id
                  ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                  : "border-gray-200 dark:border-slate-700"
              }`}
            >
              <report.icon size={24} className="mx-auto mb-2" />
              <p className="font-semibold text-gray-900 dark:text-white">
                {report.label}
              </p>
            </button>
          ))}
        </div>
      </Card>

      {/* Stats Overview */}
      <div className="grid gap-6 md:grid-cols-3 mb-8">
        <Card className="p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
            Total Revenue (This Month)
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">
            $61,000
          </p>
          <Badge className="mt-2 bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
            +27% from last month
          </Badge>
        </Card>

        <Card className="p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
            Active Users
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">
            3,890
          </p>
          <Badge className="mt-2 bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
            +24% from last month
          </Badge>
        </Card>

        <Card className="p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
            Avg Order Value
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">
            $156.80
          </p>
          <Badge className="mt-2 bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400">
            +8% from last month
          </Badge>
        </Card>
      </div>

      {/* Chart Data */}
      <Card className="p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
          Trends
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-slate-700">
                <th className="text-left py-3 px-4 font-semibold">Date</th>
                <th className="text-right py-3 px-4 font-semibold">Value</th>
                <th className="text-right py-3 px-4 font-semibold">Change</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr
                  key={idx}
                  className="border-b border-gray-200 dark:border-slate-700"
                >
                  <td className="py-3 px-4">{row.date}</td>
                  <td className="text-right py-3 px-4 font-semibold">
                    ${row.value.toLocaleString()}
                  </td>
                  <td className="text-right py-3 px-4">
                    <Badge
                      className={
                        row.change > 0
                          ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                          : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
                      }
                    >
                      {row.change > 0 ? "+" : ""}{row.change}%
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Export Options */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Export Options
        </h2>
        <div className="flex gap-4">
          <Button variant="outline">Export as CSV</Button>
          <Button variant="outline">Export as PDF</Button>
          <Button variant="outline">Schedule Report</Button>
        </div>
      </Card>
    </div>
  );
}
