"use client";

import { ProductCard } from "./ProductCard";

interface Product {
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

interface ProductGridProps {
  products: Product[];
  isLoading?: boolean;
  columns?: 2 | 3 | 4;
}

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  isLoading,
  columns = 3,
}) => {
  const gridColsClass = {
    2: "grid-cols-1 md:grid-cols-2",
    3: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
    4: "grid-cols-1 md:grid-cols-2 lg:grid-cols-4",
  };

  return (
    <div className={`grid ${gridColsClass[columns]} gap-6`}>
      {products.map((product) => (
        <ProductCard key={product.id} {...product} />
      ))}
    </div>
  );
};
