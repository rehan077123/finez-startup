"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { ProductGrid } from "@/components/product";
import { X, Plus } from "lucide-react";

interface CompareProduct {
  id: string;
  name: string;
  price: number;
  rating: number;
  specs: Record<string, string>;
}

export default function ComparePage() {
  const [products, setProducts] = useState<CompareProduct[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setProducts([
      {
        id: "1",
        name: "Product A",
        price: 99.99,
        rating: 4.5,
        specs: {
          Brand: "Brand A",
          Storage: "128GB",
          Color: "Black",
          Warranty: "1 Year",
        },
      },
      {
        id: "2",
        name: "Product B",
        price: 129.99,
        rating: 4.8,
        specs: {
          Brand: "Brand B",
          Storage: "256GB",
          Color: "White",
          Warranty: "2 Years",
        },
      },
    ]);
    setIsLoading(false);
  }, []);

  if (isLoading) return <Spinner size="lg" />;

  const allSpecs = new Set<string>();
  products.forEach((p) => {
    Object.keys(p.specs).forEach((spec) => allSpecs.add(spec));
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Compare Products
      </h1>

      <div className="overflow-x-auto">
        <table className="w-full">
          <tbody>
            <tr className="border-b border-gray-200 dark:border-slate-700">
              <td className="py-4 px-4 font-semibold text-gray-900 dark:text-white w-48">
                Name
              </td>
              {products.map((product) => (
                <td key={product.id} className="py-4 px-4 text-center">
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {product.name}
                  </p>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                      setProducts(products.filter((p) => p.id !== product.id))
                    }
                  >
                    <X size={16} /> Remove
                  </Button>
                </td>
              ))}
              {products.length < 4 && (
                <td className="py-4 px-4 text-center">
                  <Button variant="outline" size="sm">
                    <Plus size={16} className="mr-2" />
                    Add Product
                  </Button>
                </td>
              )}
            </tr>

            <tr className="border-b border-gray-200 dark:border-slate-700">
              <td className="py-4 px-4 font-semibold">Price</td>
              {products.map((product) => (
                <td key={product.id} className="py-4 px-4 text-center">
                  <p className="text-2xl font-bold text-blue-600">
                    ${product.price.toFixed(2)}
                  </p>
                </td>
              ))}
            </tr>

            <tr className="border-b border-gray-200 dark:border-slate-700">
              <td className="py-4 px-4 font-semibold">Rating</td>
              {products.map((product) => (
                <td key={product.id} className="py-4 px-4 text-center">
                  <Badge className="bg-yellow-500">
                    ⭐ {product.rating}
                  </Badge>
                </td>
              ))}
            </tr>

            {Array.from(allSpecs).map((spec) => (
              <tr
                key={spec}
                className="border-b border-gray-200 dark:border-slate-700"
              >
                <td className="py-4 px-4 font-semibold text-gray-900 dark:text-white">
                  {spec}
                </td>
                {products.map((product) => (
                  <td key={product.id} className="py-4 px-4 text-center">
                    <p className="text-gray-700 dark:text-gray-300">
                      {product.specs[spec] || "N/A"}
                    </p>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 flex gap-4 justify-center">
        {products.map((product) => (
          <Button key={product.id} className="flex-1">
            Buy {product.name}
          </Button>
        ))}
      </div>
    </div>
  );
}
