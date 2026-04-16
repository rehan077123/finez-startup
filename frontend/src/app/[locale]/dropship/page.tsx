'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, Badge } from '@/components/ui';
import { ShoppingCart, TrendingUp, AlertCircle, CheckCircle, Upload } from 'lucide-react';

const DROPSHIP_PROGRAMS = [
  {
    id: 1,
    name: 'Printful',
    logo: '🖨️',
    category: 'Print-on-Demand',
    commission: '10-50%',
    setup: 'Free',
    products: ['T-Shirts', 'Hoodies', 'Mugs', 'Phone Cases', 'Tote Bags'],
    link: 'https://www.printful.com/start',
    description: 'Create and sell custom merchandise',
    features: ['Auto-fulfillment', 'Design uploads', 'Quality guaranteed', 'Global shipping'],
    minOrder: 'No minimum',
  },
  {
    id: 2,
    name: 'Oberlo',
    logo: '🛒',
    category: 'General E-commerce',
    commission: '15-40%',
    setup: 'Free + Shopify',
    products: ['Electronics', 'Fashion', 'Home & Garden', 'Sports', 'Accessories'],
    link: 'https://www.oberlo.com/start',
    description: 'Dropship from AliExpress suppliers',
    features: ['Supplier verification', 'Auto-ordering', 'Tracking included', 'Bulk orders'],
    minOrder: 'Low minimums',
  },
  {
    id: 3,
    name: 'Spocket',
    logo: '🌐',
    category: 'Premium Dropship',
    commission: '20-50%',
    setup: '₹5000/month',
    products: ['Electronics', 'Fashion', 'Home Goods', 'Beauty', 'Gadgets'],
    link: 'https://www.spocket.co/signup',
    description: 'Dropship from US & EU suppliers',
    features: ['US/EU warehouses', 'Fast shipping', 'Quality items', 'Integration ready'],
    minOrder: 'Per item',
  },
  {
    id: 4,
    name: 'DSers',
    logo: '📊',
    category: 'Multi-Channel',
    commission: '10-45%',
    setup: 'Free',
    products: ['All categories', 'Trending items', 'Seasonal', 'Custom bundles'],
    link: 'https://www.dsers.com/login',
    description: 'Dropship to Shopify, WooCommerce, eBay',
    features: ['Multi-channel', 'Supplier network', 'Analytics', 'Automation'],
    minOrder: 'Flexible',
  },
];

const SAMPLE_PRODUCTS = [
  {
    id: 1,
    name: 'Wireless Bluetooth Earbuds',
    price: '₹1,299',
    cost: '₹399',
    image: 'https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg',
    profit: '₹900',
    rating: 4.5,
    platform: 'Oberlo',
    category: 'Electronics',
  },
  {
    id: 2,
    name: 'Custom T-Shirt with Logo',
    price: '₹499',
    cost: '₹199',
    image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop',
    profit: '₹300',
    rating: 4.8,
    platform: 'Printful',
    category: 'Fashion',
  },
  {
    id: 3,
    name: '4K Webcam',
    price: '₹4,999',
    cost: '₹1,299',
    image: 'https://m.media-amazon.com/images/I/71aDpNl1BHL._SX679_.jpg',
    profit: '₹3,700',
    rating: 4.6,
    platform: 'Spocket',
    category: 'Electronics',
  },
  {
    id: 4,
    name: 'Phone Stand (Premium)',
    price: '₹899',
    cost: '₹199',
    image: 'https://m.media-amazon.com/images/I/61Hd8lYdnnL._SX679_.jpg',
    profit: '₹700',
    rating: 4.4,
    platform: 'DSers',
    category: 'Accessories',
  },
];

export default function DropshipPage() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [vendorProducts, setVendorProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch vendor dropship products
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/api/products?type=dropship&verified=false');
        if (response.ok) {
          const data = await response.json();
          setVendorProducts(data);
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const categories = ['all', 'Electronics', 'Fashion', 'Home & Kitchen', 'Sports', 'Books', 'Health & Beauty', 'Gadgets', 'Accessories'];
  const filteredProducts = selectedCategory === 'all' 
    ? vendorProducts 
    : vendorProducts.filter(p => p.category === selectedCategory);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <div className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center gap-3 mb-2">
            <ShoppingCart className="text-blue-400" size={32} />
            <h1 className="text-4xl font-bold text-white">Dropship Programs</h1>
          </div>
          <p className="text-gray-400 ml-11">Start your online store without inventory</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <TrendingUp className="mx-auto text-green-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">{DROPSHIP_PROGRAMS.length}</div>
            <p className="text-gray-400 text-sm">Programs</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <CheckCircle className="mx-auto text-blue-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">10-50%</div>
            <p className="text-gray-400 text-sm">Commission Rate</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <AlertCircle className="mx-auto text-yellow-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">No Inventory</div>
            <p className="text-gray-400 text-sm">Required</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <ShoppingCart className="mx-auto text-purple-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">1000+</div>
            <p className="text-gray-400 text-sm">Products</p>
          </Card>
        </div>

        {/* Programs */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8">Available Programs</h2>
          <div className="space-y-6">
            {DROPSHIP_PROGRAMS.map(program => (
              <Card
                key={program.id}
                className="bg-slate-800 border-slate-700 overflow-hidden hover:border-blue-400 transition p-6"
              >
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-start">
                  {/* Program Info */}
                  <div className="md:col-span-2">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="text-5xl">{program.logo}</div>
                      <div>
                        <h3 className="text-2xl font-bold text-white">
                          {program.name}
                        </h3>
                        <p className="text-gray-400 text-sm">{program.description}</p>
                        <Badge className="mt-2 bg-blue-600">{program.category}</Badge>
                      </div>
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="space-y-2">
                    <div className="bg-slate-700 p-3 rounded">
                      <p className="text-xs text-gray-400">Commission</p>
                      <p className="text-lg font-bold text-yellow-400">
                        {program.commission}
                      </p>
                    </div>
                    <div className="bg-slate-700 p-3 rounded">
                      <p className="text-xs text-gray-400">Setup Cost</p>
                      <p className="text-lg font-bold text-white">
                        {program.setup}
                      </p>
                    </div>
                    <div className="bg-slate-700 p-3 rounded">
                      <p className="text-xs text-gray-400">Min Order</p>
                      <p className="text-lg font-bold text-white">
                        {program.minOrder}
                      </p>
                    </div>
                  </div>

                  {/* CTA */}
                  <div className="flex flex-col justify-center">
                    <a
                      href={program.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded transition text-center mb-3"
                    >
                      Join Program
                    </a>
                    <button className="w-full px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded transition text-sm">
                      View Products
                    </button>
                  </div>
                </div>

                {/* Features & Products */}
                <div className="border-t border-slate-700 mt-6 pt-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-semibold text-white mb-2">Features:</h4>
                      <ul className="space-y-1">
                        {program.features.map((feature, idx) => (
                          <li key={idx} className="text-gray-300 text-sm flex items-center">
                            <span className="text-green-400 mr-2">✓</span>
                            {feature}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-2">Product Categories:</h4>
                      <div className="flex flex-wrap gap-2">
                        {program.products.map((cat, idx) => (
                          <Badge key={idx} className="bg-slate-700 text-xs">
                            {cat}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Vendor Dropship Products Section */}
        <div className="mt-16">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-2">Vendor Dropship Products</h2>
            <p className="text-gray-400">Curated products from community dropshippers</p>
          </div>

          {/* Category Filter */}
          <div className="mb-8 flex gap-2 flex-wrap">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg transition ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
                }`}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>

          {/* Products Grid */}
          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-400">Loading products...</p>
            </div>
          ) : vendorProducts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-400 mb-4">No vendor dropship products yet</p>
              <Link href="/en/vendor/sell" className="text-blue-400 hover:text-blue-300 flex items-center justify-center gap-2">
                <Upload size={18} /> Be the first to upload →
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {filteredProducts.map(product => (
                <Card key={product.id} className="bg-slate-800 border-slate-700 overflow-hidden hover:border-blue-400 transition h-full flex flex-col">
                  {/* Product Image */}
                  {product.image_url && (
                    <div className="w-full h-48 bg-slate-700 overflow-hidden">
                      <img
                        src={product.image_url}
                        alt={product.title}
                        className="w-full h-full object-cover hover:scale-110 transition"
                        onError={(e) => {
                          e.currentTarget.src = 'https://via.placeholder.com/300x300?text=No+Image';
                        }}
                      />
                    </div>
                  )}

                  {/* Product Info */}
                  <div className="p-4 flex flex-col flex-grow">
                    <h3 className="font-semibold text-white mb-2 line-clamp-2">{product.title}</h3>
                    <p className="text-gray-400 text-sm mb-3 line-clamp-2">{product.description}</p>

                    {/* Category Badge */}
                    <div className="mb-3">
                      <Badge className="bg-blue-600 text-xs">{product.category}</Badge>
                    </div>

                    {/* Price */}
                    <div className="mb-4 flex gap-2 items-center">
                      <span className="text-xl font-bold text-blue-400">₹{product.price}</span>
                      {product.original_price && (
                        <span className="text-sm text-gray-500 line-through">₹{product.original_price}</span>
                      )}
                    </div>

                    {/* Rating */}
                    {product.rating && (
                      <div className="mb-4 text-sm">
                        <span className="text-yellow-400">★ {product.rating}</span>
                        <span className="text-gray-500"> ({product.review_count || 0})</span>
                      </div>
                    )}

                    {/* Buy Button */}
                    <a
                      href={product.link || product.affiliateLink || product.affiliate_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full mt-auto px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded transition text-center text-sm"
                    >
                      View & Order
                    </a>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Sample Products */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-white mb-8">Sample Dropship Products</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {SAMPLE_PRODUCTS.map(product => (
              <Card
                key={product.id}
                className="bg-slate-800 border-slate-700 overflow-hidden hover:border-blue-400 transition"
              >
                <div className="aspect-square overflow-hidden bg-slate-700">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-4">
                  <Badge className="bg-blue-600 text-xs mb-2">{product.platform}</Badge>
                  <h3 className="font-semibold text-white truncate">{product.name}</h3>
                  <p className="text-xs text-gray-400 mt-1">{product.category}</p>

                  <div className="mt-3 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Selling Price:</span>
                      <span className="text-yellow-400 font-bold">{product.price}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Cost:</span>
                      <span className="text-gray-400 text-sm">{product.cost}</span>
                    </div>
                    <div className="flex justify-between items-center pt-1 border-t border-slate-700">
                      <span className="text-gray-300 text-sm font-medium">Your Profit:</span>
                      <span className="text-green-400 font-bold">{product.profit}</span>
                    </div>
                  </div>

                  <div className="flex items-center mt-3">
                    <span className="text-yellow-500">⭐ {product.rating}</span>
                  </div>

                  <button className="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition text-sm">
                    Add to Store
                  </button>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-16 bg-gradient-to-r from-blue-900 to-indigo-900 rounded-lg p-12">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">How Dropshipping Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-blue-700 inline-flex items-center justify-center w-16 h-16 rounded-full mb-3">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h4 className="font-semibold text-white mb-2">Join Program</h4>
              <p className="text-gray-300 text-sm">Sign up with a dropship platform</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-700 inline-flex items-center justify-center w-16 h-16 rounded-full mb-3">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h4 className="font-semibold text-white mb-2">List Products</h4>
              <p className="text-gray-300 text-sm">Add products to your store</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-700 inline-flex items-center justify-center w-16 h-16 rounded-full mb-3">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h4 className="font-semibold text-white mb-2">Get Orders</h4>
              <p className="text-gray-300 text-sm">Customers purchase from you</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-700 inline-flex items-center justify-center w-16 h-16 rounded-full mb-3">
                <span className="text-2xl font-bold text-white">4</span>
              </div>
              <h4 className="font-semibold text-white mb-2">Earn Profit</h4>
              <p className="text-gray-300 text-sm">Keep the difference</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
