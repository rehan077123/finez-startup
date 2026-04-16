"use client";

import { Card, Badge } from "@/components/ui";
import { formatPrice, getRatingColor } from "@/utils/helpers";
import Link from "next/link";
import { Star, TrendingUp } from "lucide-react";

interface ProductCardProps {
  id: string;
  name: string;
  brand?: string;
  image?: string;
  currentPrice: number;
  originalPrice?: number;
  discountPercent?: number;
  rating?: number;
  ratingCount?: number;
  platform: string;
  inStock: boolean;
  finezScore?: number;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  id,
  name,
  brand,
  image,
  currentPrice,
  originalPrice,
  discountPercent,
  rating,
  ratingCount,
  platform,
  inStock,
  finezScore,
}) => {
  return (
    <Link href={`/product/${id}`}>
      <Card hoverable className="h-full flex flex-col">
        {/* Image */}
        {image ? (
          <div className="relative h-48 bg-gray-100 dark:bg-slate-700 rounded-lg mb-4 overflow-hidden">
            <img
              src={image}
              alt={name}
              className="w-full h-full object-contain"
            />
            {discountPercent && (
              <Badge variant="error" className="absolute top-2 right-2">
                -{discountPercent}%
              </Badge>
            )}
          </div>
        ) : (
          <div className="h-48 bg-gray-100 dark:bg-slate-700 rounded-lg mb-4 flex items-center justify-center">
            <span className="text-gray-400">No image</span>
          </div>
        )}

        {/* Content */}
        <div className="flex-1 flex flex-col">
          {/* Brand */}
          {brand && (
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">
              {brand}
            </p>
          )}

          {/* Name */}
          <h3 className="font-bold text-sm mb-2 line-clamp-2 text-gray-900 dark:text-white">
            {name}
          </h3>

          {/* Rating */}
          {rating && (
            <div className="flex items-center gap-1 mb-2">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    size={14}
                    className={
                      i < Math.floor(rating)
                        ? "fill-yellow-400 text-yellow-400"
                        : "text-gray-300"
                    }
                  />
                ))}
              </div>
              <span className={`text-xs font-bold ${getRatingColor(rating)}`}>
                {rating}
              </span>
              <span className="text-xs text-gray-500">({ratingCount})</span>
            </div>
          )}

          {/* Pricing */}
          <div className="mb-2">
            <div className="flex items-baseline gap-2">
              <span className="text-lg font-bold text-blue-600">
                {formatPrice(currentPrice)}
              </span>
              {originalPrice && (
                <span className="text-sm text-gray-400 line-through">
                  {formatPrice(originalPrice)}
                </span>
              )}
            </div>
          </div>

          {/* Platform & Score */}
          <div className="flex justify-between items-center mt-auto">
            <Badge variant="secondary">{platform}</Badge>
            {finezScore && (
              <div className="flex items-center gap-1">
                <TrendingUp size={14} className="text-green-600" />
                <span className="text-xs font-bold text-green-600">
                  {Math.round(finezScore)}
                </span>
              </div>
            )}
          </div>

          {/* Stock Status */}
          <p
            className={`text-xs font-semibold mt-2 ${
              inStock ? "text-green-600" : "text-red-600"
            }`}
          >
            {inStock ? "In Stock" : "Out of Stock"}
          </p>
        </div>
      </Card>
    </Link>
  );
};
