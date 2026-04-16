"use client";

import { useState } from "react";
import { Card, Button, Badge, Input, Spinner } from "@/components/ui";
import { Eye, EyeOff, Trash2, CheckCircle, XCircle } from "lucide-react";

interface FlaggedContent {
  id: string;
  type: "product" | "review" | "user" | "listing";
  title: string;
  reason: string;
  reportedBy: string;
  reportCount: number;
  status: "pending" | "reviewed" | "approved" | "removed";
  flaggedAt: string;
}

export default function AdminModerationPage() {
  const [items, setItems] = useState<FlaggedContent[]>([
    {
      id: "1",
      type: "product",
      title: "Suspicious Electronics Listing",
      reason: "Counterfeit product",
      reportedBy: "5",
      reportCount: 5,
      status: "pending",
      flaggedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: "2",
      type: "review",
      title: "Inappropriate Review",
      reason: "Contains offensive language",
      reportedBy: "2",
      reportCount: 2,
      status: "pending",
      flaggedAt: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: "3",
      type: "user",
      title: "Suspicious User Activity",
      reason: "Multiple fraud reports",
      reportedBy: "8",
      reportCount: 8,
      status: "reviewed",
      flaggedAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    },
  ]);

  const getStatusColor = (status: string) => {
    const colors = {
      pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
      reviewed:
        "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
      approved:
        "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
      removed: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
    };
    return colors[status as keyof typeof colors] || colors.pending;
  };

  const handleApprove = (id: string) => {
    setItems(items.map((item) => (item.id === id ? { ...item, status: "approved" } : item)));
  };

  const handleRemove = (id: string) => {
    setItems(items.map((item) => (item.id === id ? { ...item, status: "removed" } : item)));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Content Moderation
      </h1>

      {/* Filter Options */}
      <Card className="p-6 mb-8">
        <div className="grid gap-4 md:grid-cols-3">
          <Input placeholder="Search by title..." />
          <select className="px-3 py-2 border border-gray-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800">
            <option>All Types</option>
            <option>Products</option>
            <option>Reviews</option>
            <option>Users</option>
          </select>
          <select className="px-3 py-2 border border-gray-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800">
            <option>All Status</option>
            <option>Pending</option>
            <option>Reviewed</option>
            <option>Approved</option>
            <option>Removed</option>
          </select>
        </div>
      </Card>

      {/* Flagged Items */}
      <div className="space-y-4">
        {items.length === 0 ? (
          <Card className="p-12 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              No flagged content to moderate
            </p>
          </Card>
        ) : (
          items.map((item) => (
            <Card key={item.id} className="p-6">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                      {item.type}
                    </Badge>
                    <Badge className={getStatusColor(item.status)}>
                      {item.status}
                    </Badge>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                    {item.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-2">
                    <strong>Reason:</strong> {item.reason}
                  </p>
                  <p className="text-sm text-gray-500">
                    Reported by {item.reportCount} user{item.reportCount > 1 ? "s" : ""} •{" "}
                    {new Date(item.flaggedAt).toLocaleDateString()}
                  </p>
                </div>
              </div>

              {item.status === "pending" && (
                <div className="flex gap-2 pt-4 border-t border-gray-200 dark:border-slate-700">
                  <Button
                    size="sm"
                    onClick={() => handleApprove(item.id)}
                    className="flex items-center gap-2"
                  >
                    <CheckCircle size={16} />
                    Approve
                  </Button>
                  <Button
                    size="sm"
                    variant="danger"
                    onClick={() => handleRemove(item.id)}
                    className="flex items-center gap-2"
                  >
                    <XCircle size={16} />
                    Remove
                  </Button>
                  <Button size="sm" variant="outline">
                    Request Info
                  </Button>
                </div>
              )}
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
