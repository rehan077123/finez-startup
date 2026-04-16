"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { useWishlist } from "@/lib/hooks";
import { Trash2, ShoppingCart, Share2 } from "lucide-react";
import Link from "next/link";

export default function WishlistPage() {
  const { items, removeItem, clearWishlist } = useWishlist();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(false);
  }, []);

  if (isLoading) return <Spinner size="lg" />;

  if (items.length === 0) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="text-center py-20">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Your Wishlist
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-8">
            Your wishlist is empty. Start adding products!
          </p>
          <Link href="/search">
            <Button>Start Shopping</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Your Wishlist
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            {items.length} items saved
          </p>
        </div>
        <Button variant="danger" onClick={clearWishlist}>
          Clear All
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {items.map((item: any) => (
          <Card key={item.id} className="overflow-hidden">
            <div className="aspect-square bg-gray-100 dark:bg-slate-700">
              {item.image && (
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-full object-cover"
                />
              )}
            </div>
            <div className="p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                {item.name}
              </h3>
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-2">
                ${item.price?.toFixed(2)}
              </p>
              {item.originalPrice && (
                <p className="text-sm text-gray-500 line-through">
                  ${item.originalPrice?.toFixed(2)}
                </p>
              )}

              <div className="flex gap-2 mt-4">
                <Button size="sm" className="flex-1">
                  <ShoppingCart size={16} className="mr-1" />
                  Buy
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => removeItem(item.id)}
                >
                  <Trash2 size={16} />
                </Button>
                <Button size="sm" variant="outline">
                  <Share2 size={16} />
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
