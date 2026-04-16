"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { ProductGrid } from "@/components/product";
import { TrendingUp, Zap } from "lucide-react";

interface Deal {
  id: string;
  name: string;
  description: string;
  image: string;
  originalPrice: number;
  dealPrice: number;
  discount: number;
  endsAt: string;
  category: string;
  trustScore: number;
}

export default function DealsPage() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Real deals data
    setDeals([
      {
        id: "1",
        name: "Apple AirPods Pro",
        description: "Premium wireless earbuds with active noise cancellation",
        image: "https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg",
        originalPrice: 34900,
        dealPrice: 24999,
        discount: 28,
        endsAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
        category: "Electronics",
        trustScore: 4.8,
      },
      {
        id: "2",
        name: "Apple Watch Series 9",
        description: "Advanced health and fitness tracker",
        image: "https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg",
        originalPrice: 56900,
        dealPrice: 41999,
        discount: 26,
        endsAt: new Date(Date.now() + 12 * 60 * 60 * 1000).toISOString(),
        category: "Electronics",
        trustScore: 4.6,
      },
    ]);
    setIsLoading(false);
  }, []);

  if (isLoading) return <Spinner size="lg" />;

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Zap size={32} className="text-yellow-500" />
          Lightning Deals
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Limited-time offers on top products
        </p>
      </div>

      {deals.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-gray-600 dark:text-gray-400">
            No deals available right now
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {deals.map((deal) => (
            <Card key={deal.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              <div className="relative aspect-square bg-gray-100 dark:bg-slate-700 overflow-hidden">
                <img
                  src={deal.image}
                  alt={deal.name}
                  className="w-full h-full object-cover"
                />
                <Badge className="absolute top-2 right-2 bg-red-600">
                  {deal.discount}% OFF
                </Badge>
                <div className="absolute top-2 left-2">
                  <Badge variant="secondary" className="bg-yellow-500">
                    <Zap size={12} className="mr-1" />
                    Deal Ends Soon
                  </Badge>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  {deal.name}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {deal.description}
                </p>

                <div className="flex items-baseline gap-2 mt-3">
                  <span className="text-2xl font-bold text-blue-600">
                    ₹{deal.dealPrice.toLocaleString('en-IN')}
                  </span>
                  <span className="text-sm line-through text-gray-500">
                    ₹{deal.originalPrice.toLocaleString('en-IN')}
                  </span>
                </div>

                <div className="flex gap-2 mt-4">
                  <Button className="flex-1">Buy Now</Button>
                  <Button variant="outline" className="flex-1">
                    Details
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
