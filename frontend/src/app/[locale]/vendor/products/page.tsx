"use client";

import { useState } from "react";
import { Card, Button, Badge, Spinner, Input } from "@/components/ui";
import { Plus, Edit2, Trash2, Search as SearchIcon } from "lucide-react";

export default function VendorProductsPage() {
  const [products] = useState([
    {
      id: "1",
      name: "Premium Laptop",
      price: 1299.99,
      stock: 45,
      status: "active",
      sales: 234,
    },
    {
      id: "2",
      name: "Wireless Mouse",
      price: 49.99,
      stock: 120,
      status: "active",
      sales: 1203,
    },
    {
      id: "3",
      name: "USB-C Hub",
      price: 79.99,
      stock: 0,
      status: "out_of_stock",
      sales: 89,
    },
  ]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Manage Products
        </h1>
        <Button>
          <Plus size={16} className="mr-2" />
          Add New Product
        </Button>
      </div>

      <Card className="p-6 mb-8">
        <div className="flex gap-4 mb-6">
          <div className="flex-1">
            <Input placeholder="Search products..." />
          </div>
          <Button variant="outline">Filter</Button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-gray-200 dark:border-slate-700">
              <tr>
                <th className="text-left py-3 px-4 font-semibold">Product</th>
                <th className="text-left py-3 px-4 font-semibold">Price</th>
                <th className="text-left py-3 px-4 font-semibold">Stock</th>
                <th className="text-left py-3 px-4 font-semibold">Sales</th>
                <th className="text-left py-3 px-4 font-semibold">Status</th>
                <th className="text-left py-3 px-4 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr
                  key={product.id}
                  className="border-b border-gray-200 dark:border-slate-700"
                >
                  <td className="py-4 px-4">
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {product.name}
                    </p>
                  </td>
                  <td className="py-4 px-4">
                    ${product.price.toFixed(2)}
                  </td>
                  <td className="py-4 px-4">{product.stock}</td>
                  <td className="py-4 px-4">{product.sales}</td>
                  <td className="py-4 px-4">
                    <Badge
                      className={
                        product.status === "active"
                          ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                          : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
                      }
                    >
                      {product.status === "active" ? "Active" : "Out of Stock"}
                    </Badge>
                  </td>
                  <td className="py-4 px-4 flex gap-2">
                    <Button size="sm" variant="outline">
                      <Edit2 size={16} />
                    </Button>
                    <Button size="sm" variant="danger">
                      <Trash2 size={16} />
                    </Button>
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
