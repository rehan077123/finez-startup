"use client";

import { useState } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { Bell, Check, Trash2 } from "lucide-react";

interface Notification {
  id: string;
  title: string;
  message: string;
  type: "info" | "success" | "warning" | "error";
  createdAt: string;
  read: boolean;
}

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: "1",
      title: "Order Shipped",
      message: "Your order #FZ-2024-001 has been shipped",
      type: "success",
      createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      read: false,
    },
    {
      id: "2",
      title: "Price Alert",
      message: "iPhone 15 Pro price dropped to $899",
      type: "info",
      createdAt: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      read: false,
    },
    {
      id: "3",
      title: "Payment Received",
      message: "Payment for order #FZ-2024-002 confirmed",
      type: "success",
      createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      read: true,
    },
  ]);

  const getTypeColor = (type: Notification["type"]) => {
    const colors = {
      info: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
      success:
        "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
      warning:
        "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
      error: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
    };
    return colors[type];
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Bell size={32} />
          Notifications
        </h1>
        <Button variant="outline">Mark All as Read</Button>
      </div>

      <div className="space-y-4">
        {notifications.length === 0 ? (
          <Card className="p-12 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              No notifications yet
            </p>
          </Card>
        ) : (
          notifications.map((notification) => (
            <Card
              key={notification.id}
              className={`p-6 ${
                !notification.read
                  ? "bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500"
                  : ""
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {notification.title}
                    </h3>
                    <Badge className={getTypeColor(notification.type)}>
                      {notification.type}
                    </Badge>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 mb-2">
                    {notification.message}
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(notification.createdAt).toLocaleString()}
                  </p>
                </div>

                <div className="flex gap-2">
                  {!notification.read && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setNotifications(
                          notifications.map((n) =>
                            n.id === notification.id
                              ? { ...n, read: true }
                              : n
                          )
                        );
                      }}
                    >
                      <Check size={16} />
                    </Button>
                  )}
                  <Button
                    size="sm"
                    variant="danger"
                    onClick={() => {
                      setNotifications(
                        notifications.filter((n) => n.id !== notification.id)
                      );
                    }}
                  >
                    <Trash2 size={16} />
                  </Button>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
