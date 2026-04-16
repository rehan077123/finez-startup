"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { ProductGrid } from "@/components/product";
import { TrendingUp, Flame } from "lucide-react";

interface TrendingProduct {
  id: string;
  name: string;
  price: number;
  image: string;
  rating: number;
  trend: "up" | "down";
  changePercent: number;
  category: string;
}

export default function TrendingPage() {
  const [products, setProducts] = useState<TrendingProduct[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setProducts([
      {
        id: "1",
        name: "Samsung Galaxy S24 Ultra",
        price: 129999,
        image: "https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg",
        rating: 4.8,
        trend: "up",
        changePercent: 15,
        category: "Electronics",
      },
      {
        id: "2",
        name: "MacBook Pro 14 M3",
        price: 139999,
        image: "https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg",
        rating: 4.6,
        trend: "up",
        changePercent: 8,
        category: "Computers",
      },
      {
        id: "3",
        name: "Apple AirPods Pro",
        price: 24999,
        image: "https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg",
        rating: 4.5,
        trend: "down",
        changePercent: -5,
        category: "Electronics",
      },
    ]);
    setIsLoading(false);
  }, []);

  if (isLoading) return <Spinner size="lg" />;

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Flame size={32} className="text-orange-500" />
          Trending Now
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Most popular products this week
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {products.map((product) => (
          <Card
            key={product.id}
            className="overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div className="relative aspect-square bg-gray-100 dark:bg-slate-700 overflow-hidden">
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute top-2 left-2">
                <Badge
                  className={
                    product.trend === "up"
                      ? "bg-green-600"
                      : "bg-red-600"
                  }
                >
                  <TrendingUp
                    size={12}
                    className={
                      product.trend === "up" ? "" : "rotate-180"
                    }
                  />
                  {product.changePercent}%
                </Badge>
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white">
                {product.name}
              </h3>
              <p className="text-xs text-gray-500 mt-1">{product.category}</p>
              <p className="text-2xl font-bold text-blue-600 mt-2">
                ₹{product.price.toLocaleString('en-IN')}
              </p>
              <div className="flex items-center mt-3">
                <span className="text-yellow-500">⭐ {product.rating}</span>
              </div>
              <Button className="w-full mt-4">View Deal</Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
