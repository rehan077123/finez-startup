'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, Button, Badge, Spinner } from '@/components/ui';
import { Search, ShoppingCart, Heart } from 'lucide-react';

const ALL_PRODUCTS = [
  { id: '1', name: 'Apple AirPods Pro', price: 24999, originalPrice: 34900, image: 'https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg', rating: 4.5, reviews: 234, category: 'Electronics', link: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY', description: 'Premium wireless earbuds with active noise cancellation' },
  { id: '2', name: 'Samsung Galaxy S24 Ultra', price: 129999, originalPrice: 159999, image: 'https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg', rating: 4.7, reviews: 512, category: 'Electronics', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra', description: 'Latest flagship smartphone with 200MP camera' },
  { id: '3', name: 'Apple Watch Series 9', price: 41999, originalPrice: 56900, image: 'https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg', rating: 4.4, reviews: 189, category: 'Electronics', link: 'https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D', description: 'Advanced health and fitness tracker' },
  { id: '4', name: 'MacBook Pro 14 M3', price: 139999, originalPrice: 189999, image: 'https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg', rating: 4.8, reviews: 378, category: 'Electronics', link: 'https://amazon.in/s?k=MacBook+Pro+14+M3', description: 'Powerful laptop for professionals' },
  { id: '5', name: 'Dell P2423D Monitor', price: 22999, originalPrice: 35000, image: 'https://m.media-amazon.com/images/I/81rtYmXtBJL._SX679_.jpg', rating: 4.6, reviews: 145, category: 'Accessories', link: 'https://amazon.in/s?k=Dell+Monitor+24', description: '24" QHD USB-C monitor' },
  { id: '6', name: 'Corsair K95 Keyboard', price: 12999, originalPrice: 19999, image: 'https://m.media-amazon.com/images/I/71b6yBzHW7L._SX679_.jpg', rating: 4.3, reviews: 98, category: 'Accessories', link: 'https://amazon.in/s?k=Mechanical+Keyboard+RGB', description: 'Mechanical RGB keyboard' },
  { id: '7', name: 'Logitech MX Mouse', price: 8999, originalPrice: 12999, image: 'https://m.media-amazon.com/images/I/71gAH0Go3uL._SX679_.jpg', rating: 4.2, reviews: 167, category: 'Accessories', link: 'https://amazon.in/s?k=Logitech+Mouse', description: 'Advanced wireless mouse' },
  { id: '8', name: 'Anker USB-C Cable', price: 599, originalPrice: 999, image: 'https://m.media-amazon.com/images/I/61xW+eNwSML._SX679_.jpg', rating: 4.1, reviews: 456, category: 'Cables', link: 'https://amazon.in/s?k=USB+C+Cable', description: '100W USB-C cable' },
];

export default function MarketplacePage() {
  const [products, setProducts] = useState(ALL_PRODUCTS);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('featured');

  useEffect(() => {
    let filtered = ALL_PRODUCTS;

    // Filter by search
    if (searchTerm) {
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(p => p.category === selectedCategory);
    }

    // Sort
    if (sortBy === 'price-low') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
      filtered.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'rating') {
      filtered.sort((a, b) => b.rating - a.rating);
    }

    setProducts(filtered);
  }, [searchTerm, selectedCategory, sortBy]);

  const categories = ['all', 'Electronics', 'Accessories', 'Cables'];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <div className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <h1 className="text-4xl font-bold text-white mb-2">Marketplace</h1>
          <p className="text-gray-400">Browse all products from top platforms</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search products, brands, categories..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-yellow-400"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card className="p-6 bg-slate-800 border-slate-700">
              <h3 className="font-semibold text-white mb-4">Filters</h3>

              {/* Category Filter */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-300 mb-3">Category</h4>
                <div className="space-y-2">
                  {categories.map(cat => (
                    <label key={cat} className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="category"
                        value={cat}
                        checked={selectedCategory === cat}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="mr-3"
                      />
                      <span className="text-gray-300 capitalize">{cat}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Sort */}
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-3">Sort By</h4>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded text-white"
                >
                  <option value="featured">Featured</option>
                  <option value="price-low">Price: Low to High</option>
                  <option value="price-high">Price: High to Low</option>
                  <option value="rating">Highest Rated</option>
                </select>
              </div>
            </Card>
          </div>

          {/* Products Grid */}
          <div className="lg:col-span-3">
            {products.length === 0 ? (
              <div className="text-center py-20">
                <p className="text-gray-400 text-lg">No products found</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map(product => (
                  <Card key={product.id} className="overflow-hidden bg-slate-800 border-slate-700 hover:border-yellow-400 transition">
                    <div className="relative aspect-square overflow-hidden bg-slate-700">
                      <img
                        src={product.image}
                        alt={product.name}
                        className="w-full h-full object-cover"
                      />
                      <Badge className="absolute top-2 right-2 bg-green-600">
                        {Math.round((1 - product.price / product.originalPrice) * 100)}% OFF
                      </Badge>
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-white truncate">{product.name}</h3>
                      <p className="text-xs text-gray-400 mt-1">{product.category}</p>

                      <div className="flex items-baseline gap-2 mt-2">
                        <span className="text-xl font-bold text-yellow-400">
                          ₹{product.price.toLocaleString('en-IN')}
                        </span>
                        <span className="text-sm line-through text-gray-500">
                          ₹{product.originalPrice.toLocaleString('en-IN')}
                        </span>
                      </div>

                      <div className="flex items-center gap-2 mt-2">
                        <span className="text-yellow-500">⭐ {product.rating}</span>
                        <span className="text-xs text-gray-400">({product.reviews})</span>
                      </div>

                      <div className="flex gap-2 mt-4">
                        <button
                          onClick={() => window.open(`/product/${product.id}`, '_blank')}
                          className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition"
                        >
                          View Details
                        </button>
                        <a
                          href={product.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex-1 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white text-sm rounded transition text-center"
                        >
                          Buy Now
                        </a>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
