"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { ProductGrid } from "@/components/product";
import { ChevronDown } from "lucide-react";

interface Category {
  id: string;
  name: string;
  icon: string;
  count: number;
  subcategories: string[];
}

export default function CategoryPage({
  params,
}: {
  params: { category: string };
}) {
  const [products, setProducts] = useState<any[]>([]);
  const [selectedSubcategory, setSelectedSubcategory] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Real products
    setProducts([
      {
        id: "1",
        name: "Apple AirPods Pro",
        price: 24999,
        image: "https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg",
        rating: 4.5,
        reviews: 128,
        link: "https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY",
      },
      {
        id: "2",
        name: "Samsung Galaxy S24 Ultra",
        price: 129999,
        image: "https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg",
        rating: 4.8,
        reviews: 256,
        link: "https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra",
      },
      {
        id: "3",
        name: "MacBook Pro 14 M3",
        price: 139999,
        image: "https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg",
        rating: 4.7,
        reviews: 340,
        link: "https://amazon.in/s?k=MacBook+Pro+14+M3",
      },
      {
        id: "4",
        name: "Apple Watch Series 9",
        price: 41999,
        image: "https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg",
        rating: 4.6,
        reviews: 192,
        link: "https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D",
      },
    ]);
    setIsLoading(false);
  }, [params.category, selectedSubcategory]);

  if (isLoading) return <Spinner size="lg" />;

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white capitalize">
          {params.category}
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Browse products in {params.category}
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-4">
        {/* Sidebar Filters */}
        <div className="lg:col-span-1">
          <Card className="p-6">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
              Filters
            </h3>
            {/* Price range, ratings, etc. */}
          </Card>
        </div>

        {/* Products Grid */}
        <div className="lg:col-span-3">
          <ProductGrid products={products} columns={3} />
        </div>
      </div>
    </div>
  );
}
