"use client";

import { ProductGrid } from "@/components/product";
import { Spinner } from "@/components/ui";

interface ResultsContainerProps {
  products: any[];
  isLoading?: boolean;
  isEmpty?: boolean;
  totalCount?: number;
  currentPage?: number;
  gridColumns?: 2 | 3 | 4;
}

export const ResultsContainer: React.FC<ResultsContainerProps> = ({
  products,
  isLoading,
  isEmpty,
  totalCount = 0,
  currentPage = 1,
  gridColumns = 3,
}) => {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  if (isEmpty || products.length === 0) {
    return (
      <div className="text-center py-20">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          No products found
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Try adjusting your search or filters
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Showing {products.length} results
        {totalCount > 0 && ` of ${totalCount.toLocaleString()}`}
      </p>
      <ProductGrid products={products} columns={gridColumns} />
    </div>
  );
};
