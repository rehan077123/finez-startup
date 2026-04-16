"use client";

import { Badge } from "@/components/ui";
import { formatPrice } from "@/utils/helpers";

interface PriceListing {
  platform: string;
  price: number;
  originalPrice?: number;
  inStock: boolean;
  url?: string;
  savings?: string;
}

interface PriceComparisonProps {
  prices: PriceListing[];
  lowestPrice?: PriceListing;
}

export const PriceComparison: React.FC<PriceComparisonProps> = ({
  prices,
  lowestPrice,
}) => {
  return (
    <div className="space-y-3">
      <h3 className="font-bold text-gray-900 dark:text-white">Price Across Platforms</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {prices.map((listing) => (
          <div
            key={listing.platform}
            className={`p-4 rounded-lg border-2 transition-all ${
              lowestPrice?.platform === listing.platform
                ? "border-green-500 bg-green-50 dark:bg-green-900/10"
                : "border-gray-200 dark:border-slate-700 hover:border-gray-300 dark:hover:border-slate-600"
            }`}
          >
            <div className="flex items-start justify-between mb-2">
              <span className="font-semibold text-gray-900 dark:text-white">
                {listing.platform}
              </span>
              {!listing.inStock && (
                <Badge variant="error">Out of Stock</Badge>
              )}
              {lowestPrice?.platform === listing.platform && (
                <Badge variant="success">Lowest</Badge>
              )}
            </div>

            <div className="space-y-2">
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold text-blue-600">
                  {formatPrice(listing.price)}
                </span>
                {listing.originalPrice && (
                  <span className="text-sm text-gray-400 line-through">
                    {formatPrice(listing.originalPrice)}
                  </span>
                )}
              </div>

              {listing.savings && (
                <p className="text-sm text-green-600 dark:text-green-400">
                  Save {listing.savings}
                </p>
              )}

              {listing.url && (
                <a
                  href={listing.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block text-sm text-blue-600 hover:underline dark:text-blue-400 mt-2"
                >
                  View on {listing.platform}
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
