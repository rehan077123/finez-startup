"use client";

import { useState } from "react";
import { Card, Button, Input, Badge, Spinner } from "@/components/ui";
import { Search as SearchIcon, Edit2, Trash2, Ban } from "lucide-react";

export default function AdminUsersPage() {
  const [users] = useState([
    {
      id: "1",
      email: "user1@example.com",
      name: "John Doe",
      role: "user",
      status: "active",
      createdAt: "2024-01-15",
      orders: 5,
    },
    {
      id: "2",
      email: "user2@example.com",
      name: "Jane Smith",
      role: "vendor",
      status: "active",
      createdAt: "2024-02-10",
      orders: 0,
    },
    {
      id: "3",
      email: "user3@example.com",
      name: "Bob Johnson",
      role: "user",
      status: "suspended",
      createdAt: "2024-01-20",
      orders: 12,
    },
  ]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Manage Users
      </h1>

      <Card className="p-6 mb-8">
        <div className="flex gap-4 mb-6">
          <div className="flex-1">
            <Input placeholder="Search users..." />
          </div>
          <Button variant="outline">Filter</Button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-gray-200 dark:border-slate-700">
              <tr>
                <th className="text-left py-3 px-4 font-semibold">Email</th>
                <th className="text-left py-3 px-4 font-semibold">Name</th>
                <th className="text-left py-3 px-4 font-semibold">Role</th>
                <th className="text-left py-3 px-4 font-semibold">Orders</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-left py-3 px-4 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr
                  key={user.id}
                  className="border-b border-gray-200 dark:border-slate-700"
                >
                  <td className="py-4 px-4">{user.email}</td>
                  <td className="py-4 px-4">
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {user.name}
                    </p>
                  </td>
                  <td className="py-4 px-4 capitalize">{user.role}</td>
                  <td className="py-4 px-4">{user.orders}</td>
                  <td className="py-4 px-4">
                    <Badge
                      className={
                        user.status === "active"
                          ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                          : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
                      }
                    >
                      {user.status}
                    </Badge>
                  </td>
                  <td className="py-4 px-4 flex gap-2">
                    <Button size="sm" variant="outline">
                      <Edit2 size={16} />
                    </Button>
                    {user.status === "active" && (
                      <Button size="sm" variant="danger">
                        <Ban size={16} />
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
