"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner, Input } from "@/components/ui";
import { Package, Check, Clock, AlertCircle } from "lucide-react";

interface Order {
  id: string;
  orderNumber: string;
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  totalAmount: number;
  items: number;
  orderDate: string;
  estimatedDelivery?: string;
  trackingNumber?: string;
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setOrders([
      {
        id: "1",
        orderNumber: "FZ-2024-001",
        status: "delivered",
        totalAmount: 245.99,
        items: 3,
        orderDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        trackingNumber: "TRK-12345678",
      },
      {
        id: "2",
        orderNumber: "FZ-2024-002",
        status: "shipped",
        totalAmount: 129.99,
        items: 1,
        orderDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
        estimatedDelivery: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
        trackingNumber: "TRK-87654321",
      },
    ]);
    setIsLoading(false);
  }, []);

  const getStatusIcon = (status: Order["status"]) => {
    switch (status) {
      case "delivered":
        return <Check size={20} className="text-green-600" />;
      case "shipped":
        return <Package size={20} className="text-blue-600" />;
      case "processing":
        return <Clock size={20} className="text-yellow-600" />;
      case "cancelled":
        return <AlertCircle size={20} className="text-red-600" />;
      default:
        return null;
    }
  };

  const getStatusBadge = (status: Order["status"]) => {
    const variants = {
      pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
      processing:
        "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
      shipped:
        "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400",
      delivered:
        "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
      cancelled:
        "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
    };
    return (
      <Badge className={`capitalize ${variants[status]}`}>
        {status}
      </Badge>
    );
  };

  if (isLoading) return <Spinner size="lg" />;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Your Orders
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Track and manage your purchases
        </p>
      </div>

      <div className="mb-8">
        <Input placeholder="Search orders..." />
      </div>

      <div className="space-y-4">
        {orders.length === 0 ? (
          <Card className="p-12 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              No orders found
            </p>
          </Card>
        ) : (
          orders.map((order) => (
            <Card key={order.id} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-4">
                  {getStatusIcon(order.status)}
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Order {order.orderNumber}
                    </p>
                    <p className="font-semibold text-gray-900 dark:text-white">
                      ${order.totalAmount.toFixed(2)}
                    </p>
                  </div>
                </div>
                {getStatusBadge(order.status)}
              </div>

              <div className="grid grid-cols-3 gap-4 py-4 border-t border-b border-gray-200 dark:border-slate-700">
                <div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    Items
                  </p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {order.items}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    Order Date
                  </p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {new Date(order.orderDate).toLocaleDateString()}
                  </p>
                </div>
                {order.trackingNumber && (
                  <div>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      Tracking
                    </p>
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {order.trackingNumber}
                    </p>
                  </div>
                )}
              </div>

              <div className="mt-4 flex gap-2">
                <Button>View Details</Button>
                {order.status === "delivered" && (
                  <Button variant="outline">Leave Review</Button>
                )}
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
