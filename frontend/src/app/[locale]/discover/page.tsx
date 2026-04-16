'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, Button, Badge } from '@/components/ui';
import { TrendingUp, Flame } from 'lucide-react';

const TRENDING_PRODUCTS = [
  { id: '1', name: 'Apple AirPods Pro', price: 24999, originalPrice: 34900, image: 'https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg', rating: 4.5, reviews: 234, category: 'Electronics', link: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY', trend: 'up', change: 15 },
  { id: '2', name: 'Samsung Galaxy S24 Ultra', price: 129999, originalPrice: 159999, image: 'https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg', rating: 4.7, reviews: 512, category: 'Electronics', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra', trend: 'up', change: 22 },
  { id: '3', name: 'Apple Watch Series 9', price: 41999, originalPrice: 56900, image: 'https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg', rating: 4.4, reviews: 189, category: 'Electronics', link: 'https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D', trend: 'up', change: 18 },
  { id: '4', name: 'MacBook Pro 14 M3', price: 139999, originalPrice: 189999, image: 'https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg', rating: 4.8, reviews: 378, category: 'Electronics', link: 'https://amazon.in/s?k=MacBook+Pro+14+M3', trend: 'up', change: 25 },
  { id: '5', name: 'Dell P2423D Monitor', price: 22999, originalPrice: 35000, image: 'https://m.media-amazon.com/images/I/81rtYmXtBJL._SX679_.jpg', rating: 4.6, reviews: 145, category: 'Accessories', link: 'https://amazon.in/s?k=Dell+Monitor+24', trend: 'up', change: 12 },
  { id: '6', name: 'Corsair K95 Keyboard', price: 12999, originalPrice: 19999, image: 'https://m.media-amazon.com/images/I/71b6yBzHW7L._SX679_.jpg', rating: 4.3, reviews: 98, category: 'Accessories', link: 'https://amazon.in/s?k=Mechanical+Keyboard+RGB', trend: 'down', change: -5 },
  { id: '7', name: 'Logitech MX Mouse', price: 8999, originalPrice: 12999, image: 'https://m.media-amazon.com/images/I/71gAH0Go3uL._SX679_.jpg', rating: 4.2, reviews: 167, category: 'Accessories', link: 'https://amazon.in/s?k=Logitech+Mouse', trend: 'up', change: 8 },
  { id: '8', name: 'Anker USB-C Cable', price: 599, originalPrice: 999, image: 'https://m.media-amazon.com/images/I/61xW+eNwSML._SX679_.jpg', rating: 4.1, reviews: 456, category: 'Cables', link: 'https://amazon.in/s?k=USB+C+Cable', trend: 'up', change: 10 },
];

export default function DiscoverPage() {
  const [products] = useState(TRENDING_PRODUCTS);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <div className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center gap-3 mb-2">
            <Flame className="text-orange-500" size={32} />
            <h1 className="text-4xl font-bold text-white">Discover Trending</h1>
          </div>
          <p className="text-gray-400 ml-11">Most popular and trending products this week</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Featured Section */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-8">🔥 Top Trending This Week</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((product: any) => (
              <Card
                key={product.id}
                className="overflow-hidden bg-slate-800 border-slate-700 hover:border-yellow-400 transition group"
              >
                <div className="relative aspect-square overflow-hidden bg-slate-700">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition"
                  />
                  <div className="absolute top-2 left-2 flex gap-2">
                    <Badge className="bg-orange-600">
                      <Flame size={12} className="mr-1" />
                      Trending
                    </Badge>
                    <Badge
                      className={
                        product.trend === 'up' ? 'bg-green-600' : 'bg-red-600'
                      }
                    >
                      <TrendingUp
                        size={12}
                        className={`mr-1 ${
                          product.trend === 'down' ? 'rotate-180' : ''
                        }`}
                      />
                      {product.change}%
                    </Badge>
                  </div>
                  <Badge className="absolute top-2 right-2 bg-yellow-600">
                    {Math.round(
                      (1 - product.price / product.originalPrice) * 100
                    )}% OFF
                  </Badge>
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-white truncate">
                    {product.name}
                  </h3>
                  <p className="text-xs text-gray-400 mt-1">{product.category}</p>

                  <div className="flex items-baseline gap-2 mt-3">
                    <span className="text-2xl font-bold text-yellow-400">
                      ₹{product.price.toLocaleString('en-IN')}
                    </span>
                    <span className="text-xs line-through text-gray-500">
                      ₹{product.originalPrice.toLocaleString('en-IN')}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-yellow-500">⭐ {product.rating}</span>
                    <span className="text-xs text-gray-400">
                      ({product.reviews})
                    </span>
                  </div>

                  <div className="flex gap-2 mt-4">
                    <Link
                      href={`/product/${product.id}`}
                      className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition text-center"
                    >
                      Explore
                    </Link>
                    <a
                      href={product.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white text-sm rounded transition text-center"
                    >
                      Buy
                    </a>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Category Sections */}
        <div className="space-y-16">
          {['Electronics', 'Accessories'].map((category) => (
            <div key={category}>
              <h2 className="text-2xl font-bold text-white mb-8">
                {category} Category
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {products
                  .filter((p: any) => p.category === category)
                  .map((product: any) => (
                    <Card
                      key={product.id}
                      className="overflow-hidden bg-slate-800 border-slate-700 hover:border-yellow-400 transition"
                    >
                      <div className="relative aspect-square overflow-hidden bg-slate-700">
                        <img
                          src={product.image}
                          alt={product.name}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="p-4">
                        <h3 className="font-semibold text-white truncate">
                          {product.name}
                        </h3>
                        <p className="text-2xl font-bold text-yellow-400 mt-2">
                          ₹{product.price.toLocaleString('en-IN')}
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <span className="text-yellow-500">⭐ {product.rating}</span>
                        </div>
                        <button
                          onClick={() =>
                            window.open(
                              `/product/${product.id}`,
                              '_blank'
                            )
                          }
                          className="w-full mt-4 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition"
                        >
                          View Details
                        </button>
                      </div>
                    </Card>
                  ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
