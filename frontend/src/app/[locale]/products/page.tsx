'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useProducts } from '@/lib/hooks';
import { formatCurrency } from '@/lib/utils';

const CATEGORIES = [
  'All',
  'AI Tools',
  'Tech',
  'Side Hustles',
  'Learning',
  'Fitness',
];

export default function ProductsPage() {
  const [category, setCategory] = useState('All');
  const [page, setPage] = useState(0);
  const limit = 20;
  const offset = page * limit;

  const { products, loading, error } = useProducts(
    category === 'All' ? undefined : category,
    limit,
    offset
  );

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-slate-900 text-white py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-2">Discover Products</h1>
          <p className="text-slate-300">
            Curated products for your lifestyle
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Category Filter */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">Categories</h2>
          <div className="flex gap-2 flex-wrap">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => {
                  setCategory(cat);
                  setPage(0);
                }}
                className={`px-4 py-2 rounded-lg transition ${
                  category === cat
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-200 text-slate-900 hover:bg-slate-300'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            Error loading products: {error.message}
          </div>
        )}

        {/* Products Grid */}
        {products && !loading && (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {products.products?.map((product: any) => (
                <div
                  key={product.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition"
                >
                  {/* Product Image */}
                  {product.image_url && (
                    <div className="relative h-48 bg-slate-100">
                      <Image
                        src={product.image_url}
                        alt={product.name}
                        fill
                        className="object-cover"
                        onError={(e) => {
                          e.currentTarget.src = '/placeholder.png';
                        }}
                      />
                    </div>
                  )}

                  {/* Product Info */}
                  <div className="p-4">
                    <h3 className="font-semibold text-lg mb-2 line-clamp-2">
                      {product.name}
                    </h3>

                    <p className="text-slate-600 text-sm mb-3 line-clamp-2">
                      {product.description}
                    </p>

                    <div className="flex items-center justify-between mb-4">
                      <span className="text-2xl font-bold text-blue-600">
                        {formatCurrency(product.price)}
                      </span>
                      {product.category && (
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          {product.category}
                        </span>
                      )}
                    </div>

                    {/* Buy Now Button */}
                    {product.link ? (
                      <a
                        href={product.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded text-center transition"
                      >
                        Buy Now
                      </a>
                    ) : (
                      <button className="w-full bg-gray-400 text-white font-semibold py-2 rounded cursor-not-allowed">
                        Buy Now
                      </button>
                    )}

                    {/* Additional Actions */}
                    <div className="mt-3 flex gap-2">
                      <button className="flex-1 text-sm px-3 py-1 border border-slate-300 rounded hover:bg-slate-50 transition">
                        Save
                      </button>
                      <button className="flex-1 text-sm px-3 py-1 border border-slate-300 rounded hover:bg-slate-50 transition">
                        Alert
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {products.total > limit && (
              <div className="flex justify-center items-center gap-4">
                <button
                  onClick={() => setPage(Math.max(0, page - 1))}
                  disabled={page === 0}
                  className="px-4 py-2 bg-slate-200 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-300"
                >
                  Previous
                </button>

                <span className="text-sm text-slate-600">
                  Page {page + 1} of {Math.ceil(products.total / limit)}
                </span>

                <button
                  onClick={() =>
                    setPage(
                      Math.min(
                        Math.ceil(products.total / limit) - 1,
                        page + 1
                      )
                    )
                  }
                  disabled={offset + limit >= products.total}
                  className="px-4 py-2 bg-slate-200 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-300"
                >
                  Next
                </button>
              </div>
            )}

            {/* Empty State */}
            {products.products?.length === 0 && (
              <div className="text-center py-12">
                <p className="text-slate-600 text-lg">
                  No products found in this category
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
