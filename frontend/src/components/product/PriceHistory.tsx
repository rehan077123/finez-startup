"use client";

interface PricePoint {
  date: string;
  price: number;
  platform?: string;
}

interface PriceHistoryProps {
  prices: PricePoint[];
  currentPrice: number;
  lowestPrice?: number;
  highestPrice?: number;
}

export const PriceHistory: React.FC<PriceHistoryProps> = ({
  prices,
  currentPrice,
  lowestPrice,
  highestPrice,
}) => {
  // Simple ASCII chart
  const maxPrice = Math.max(...prices.map((p) => p.price));
  const minPrice = Math.min(...prices.map((p) => p.price));
  const range = maxPrice - minPrice || 1;

  return (
    <div className="space-y-4">
      <h3 className="font-bold text-gray-900 dark:text-white">Price Trend (Last 30 days)</h3>

      {/* Mini Stats */}
      <div className="grid grid-cols-3 gap-3">
        <div className="p-3 bg-blue-50 dark:bg-blue-900/10 rounded-lg">
          <p className="text-xs text-gray-600 dark:text-gray-400">Current</p>
          <p className="text-lg font-bold text-blue-600">₹{currentPrice.toLocaleString()}</p>
        </div>
        {lowestPrice && (
          <div className="p-3 bg-green-50 dark:bg-green-900/10 rounded-lg">
            <p className="text-xs text-gray-600 dark:text-gray-400">Lowest</p>
            <p className="text-lg font-bold text-green-600">₹{lowestPrice.toLocaleString()}</p>
          </div>
        )}
        {highestPrice && (
          <div className="p-3 bg-red-50 dark:bg-red-900/10 rounded-lg">
            <p className="text-xs text-gray-600 dark:text-gray-400">Highest</p>
            <p className="text-lg font-bold text-red-600">₹{highestPrice.toLocaleString()}</p>
          </div>
        )}
      </div>

      {/* Price List */}
      <div className="space-y-1 text-sm max-h-32 overflow-y-auto">
        {prices.slice(-7).reverse().map((point, idx) => {
          const height = ((point.price - minPrice) / range * 100) || 0;
          return (
            <div key={idx} className="flex items-center gap-2">
              <span className="w-20 text-gray-600 dark:text-gray-400 text-xs">
                {point.date}
              </span>
              <div className="flex-1 h-6 bg-gray-100 dark:bg-slate-700 rounded relative">
                <div
                  className="h-full bg-blue-500 rounded transition-all"
                  style={{ width: `${height}%` }}
                />
              </div>
              <span className="w-20 text-right font-medium text-gray-900 dark:text-white">
                ₹{point.price.toLocaleString()}
              </span>
            </div>
          );
        })}
      </div>

      <p className="text-xs text-gray-500 dark:text-gray-500">
        Data from last 30 days • Prices updated daily
      </p>
    </div>
  );
};
