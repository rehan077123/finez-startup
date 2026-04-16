"use client";

import { useState, useEffect } from "react";
import { Card, Button, Spinner, Badge } from "@/components/ui";
import { ProductGrid } from "@/components/product";
import { Heart, Share2 } from "lucide-react";

export default function ProductDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const [product, setProduct] = useState<any>(null);
  const [inWishlist, setInWishlist] = useState(false);

  useEffect(() => {
    // Real product fetch
    setProduct({
      id: params.id,
      name: "Apple AirPods Pro",
      price: 24999,
      originalPrice: 34900,
      rating: 4.8,
      reviews: 1234,
      description:
        "Premium wireless earbuds with active noise cancellation. Perfect for music lovers and professionals.",
      image: "https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg",
      images: ["https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg", "https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg"],
      specs: {
        Brand: "Apple",
        Model: "MLWK3HN/A",
        Color: "White",
        "Noise Cancellation": "Active",
        "Battery Life": "6 hours (30 with case)",
        Connectivity: "Bluetooth 5.3",
        "Built-in Mic": "Yes",
      },
      inStock: true,
      availability: {
        amazon: 24999,
        flipkart: 25999,
        croma: 26999,
        reliancedigital: 25499,
      },
    });
  }, [params.id]);

  if (!product) return <Spinner size="lg" />;

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="grid gap-12 md:grid-cols-2">
        {/* Images */}
        <div>
          <div className="bg-gray-100 dark:bg-slate-700 rounded-lg mb-4 aspect-square flex items-center justify-center">
            <img
              src={product.image}
              alt={product.name}
              className="max-w-full max-h-full"
            />
          </div>
          <div className="grid grid-cols-4 gap-2">
            {product.images.map((img: string, idx: number) => (
              <button
                key={idx}
                className="bg-gray-100 dark:bg-slate-700 rounded-lg aspect-square"
              >
                <img src={img} alt={`View ${idx + 1}`} />
              </button>
            ))}
          </div>
        </div>

        {/* Details */}
        <div>
          <div className="mb-4 flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                {product.name}
              </h1>
              <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                <span>⭐ {product.rating}</span>
                <span>({product.reviews.toLocaleString()} reviews)</span>
              </div>
            </div>
            <Button
              variant="outline"
              size="lg"
              onClick={() => setInWishlist(!inWishlist)}
            >
              <Heart
                size={20}
                className={inWishlist ? "fill-red-600 text-red-600" : ""}
              />
            </Button>
          </div>

          <div className="mb-6 pb-6 border-b border-gray-200 dark:border-slate-700">
            <p className="text-4xl font-bold text-blue-600 mb-2">
              ₹{product.price.toLocaleString('en-IN')}
            </p>
            {product.originalPrice && (
              <p className="text-lg line-through text-gray-500">
                ₹{product.originalPrice.toLocaleString('en-IN')}
              </p>
            )}
            <Badge className="mt-2 bg-green-600">In Stock</Badge>
          </div>

          <p className="text-gray-700 dark:text-gray-300 mb-6">
            {product.description}
          </p>

          <div className="space-y-3 mb-8">
            <Button className="w-full" size="lg">
              Buy Now
            </Button>
            <Button
              className="w-full"
              variant="outline"
              size="lg"
              onClick={() => alert("Work with this to add to cart!")}
            >
              Add to Cart
            </Button>
            <Button
              className="w-full"
              variant="outline"
              size="lg"
            >
              <Share2 size={16} className="mr-2" />
              Share
            </Button>
          </div>

          {/* Price Comparison */}
          <Card className="p-6">
            <h3 className="font-bold text-gray-900 dark:text-white mb-4">
              Price on Other Platforms
            </h3>
            <div className="space-y-3">
              {Object.entries(product.availability).map(([site, price]) => (
                <div
                  key={site}
                  className="flex justify-between items-center p-3 bg-gray-50 dark:bg-slate-700/50 rounded"
                >
                  <span className="capitalize font-semibold text-gray-900 dark:text-white">
                    {site}
                  </span>
                  <span className="font-bold text-blue-600">
                    ${(price as number).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* Specs Table */}
      <Card className="p-6 mt-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Specifications
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <tbody>
              {Object.entries(product.specs).map(([key, value], idx) => (
                <tr
                  key={key}
                  className={`border-b border-gray-200 dark:border-slate-700 ${
                    idx % 2 === 0
                      ? "bg-gray-50 dark:bg-slate-700/30"
                      : ""
                  }`}
                >
                  <td className="py-3 px-4 font-semibold text-gray-900 dark:text-white">
                    {key}
                  </td>
                  <td className="py-3 px-4 text-gray-700 dark:text-gray-300">
                    {value as string}
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
