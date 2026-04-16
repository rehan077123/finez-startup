'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, Badge, Button } from '@/components/ui';
import { Users, TrendingUp, Zap, Gift, ShoppingCart } from 'lucide-react';

const AFFILIATE_PLATFORMS = [
  {
    id: 1,
    name: 'Amazon Associates',
    logo: '🛍️',
    commission: '1-10%',
    minPayout: '$100',
    cookieDuration: '24 hours',
    description: 'Earn commissions on products sold through your links',
    link: 'https://affiliate-program.amazon.in/home',
    benefits: ['Largest product catalog', 'Real-time tracking', 'Multiple payment options'],
    products: [
      { name: 'Samsung Galaxy S24', commission: '3-5%', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24' },
      { name: 'MacBook Pro 14', commission: '2-5%', link: 'https://amazon.in/s?k=MacBook+Pro+14' },
      { name: 'Apple AirPods Pro', commission: '4-6%', link: 'https://amazon.in/Apple-AirPods-Pro/s' },
    ],
  },
  {
    id: 2,
    name: 'Flipkart Affiliate',
    logo: '📦',
    commission: '0.5-10%',
    minPayout: '₹500',
    cookieDuration: '30 days',
    description: 'Join India\'s largest e-commerce affiliate program',
    link: 'https://affiliate.flipkart.com',
    benefits: ['30-day cookie', 'Fast approvals', 'Weekly payouts', 'Real-time dashboard'],
    products: [
      { name: 'Smartphones', commission: '2-4%', link: 'https://flipkart.com/search?q=smartphones' },
      { name: 'Laptops & CPUs', commission: '1-3%', link: 'https://flipkart.com/search?q=laptops' },
      { name: 'Accessories', commission: '5-10%', link: 'https://flipkart.com/search?q=accessories' },
    ],
  },
  {
    id: 3,
    name: 'CJaffiliate.com',
    logo: '🤝',
    commission: '2-15%',
    minPayout: '$100',
    cookieDuration: '45 days',
    description: 'Global network of merchants and publishers',
    link: 'https://www.cjaffiliates.com',
    benefits: ['450+ merchants', 'Global reach', 'Premium support', 'Weekly reports'],
    products: [
      { name: 'Tech Products', commission: '5-15%', link: 'https://www.cjaffiliates.com/home' },
      { name: 'Digital Services', commission: '10-20%', link: 'https://www.cjaffiliates.com/home' },
      { name: 'Home & Garden', commission: '8-12%', link: 'https://www.cjaffiliates.com/home' },
    ],
  },
  {
    id: 4,
    name: 'ShareASale',
    logo: '💰',
    commission: '5-30%',
    minPayout: '$20',
    cookieDuration: '30 days',
    description: 'Premium affiliate network with 4000+ merchants',
    link: 'https://shareasale.com',
    benefits: ['4000+ merchants', 'Easy tracking', 'Real-time reporting', 'Multiple categories'],
    products: [
      { name: 'Electronics', commission: '5-15%', link: 'https://shareasale.com' },
      { name: 'Software', commission: '15-30%', link: 'https://shareasale.com' },
      { name: 'Online Services', commission: '10-25%', link: 'https://shareasale.com' },
    ],
  },
];

export default function AffiliatePage() {
  const [vendorProducts, setVendorProducts] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch vendor affiliate products
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/api/products?type=affiliate&verified=false&provider=affiliate');
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

  const categories = ['All', 'Electronics', 'Fashion', 'Home & Kitchen', 'Sports', 'Books', 'Health & Beauty', 'Gadgets', 'Accessories'];
  const filteredProducts = selectedCategory === 'All' 
    ? vendorProducts 
    : vendorProducts.filter(p => p.category === selectedCategory);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <div className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center gap-3 mb-2">
            <Users className="text-green-400" size={32} />
            <h1 className="text-4xl font-bold text-white">Affiliate Programs</h1>
          </div>
          <p className="text-gray-400 ml-11">Earn money by promoting products and services</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Affiliate Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <Gift className="mx-auto text-green-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">{AFFILIATE_PLATFORMS.length}</div>
            <p className="text-gray-400 text-sm">Programs</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <TrendingUp className="mx-auto text-blue-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">5-30%</div>
            <p className="text-gray-400 text-sm">Avg Commission</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <Zap className="mx-auto text-yellow-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">4K+</div>
            <p className="text-gray-400 text-sm">Merchants</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <Users className="mx-auto text-purple-400 mb-3" size={32} />
            <div className="text-2xl font-bold text-white">100K+</div>
            <p className="text-gray-400 text-sm">Affiliates</p>
          </Card>
        </div>

        {/* Platforms */}
        <div className="space-y-6">
          {AFFILIATE_PLATFORMS.map(platform => (
            <Card
              key={platform.id}
              className="bg-slate-800 border-slate-700 overflow-hidden hover:border-green-400 transition p-6"
            >
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                {/* Platform Info */}
                <div className="md:col-span-2">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="text-5xl">{platform.logo}</div>
                    <div>
                      <h3 className="text-2xl font-bold text-white">
                        {platform.name}
                      </h3>
                      <p className="text-gray-400 text-sm">{platform.description}</p>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-3">
                    {platform.benefits.map((benefit, idx) => (
                      <Badge key={idx} className="bg-green-600 text-xs">
                        {benefit}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Stats */}
                <div className="space-y-3">
                  <div className="bg-slate-700 p-3 rounded">
                    <p className="text-xs text-gray-400">Commission Rate</p>
                    <p className="text-lg font-bold text-yellow-400">
                      {platform.commission}
                    </p>
                  </div>
                  <div className="bg-slate-700 p-3 rounded">
                    <p className="text-xs text-gray-400">Min Payout</p>
                    <p className="text-lg font-bold text-white">
                      {platform.minPayout}
                    </p>
                  </div>
                </div>

                {/* Join Button */}
                <div className="flex flex-col justify-between">
                  <a
                    href={platform.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded transition text-center"
                  >
                    Join Now
                  </a>
                </div>
              </div>

              {/* Products in Program */}
              <div className="border-t border-slate-700 pt-6">
                <h4 className="font-semibold text-white mb-4">
                  Popular Products:
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {platform.products.map((product, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-700 p-4 rounded border border-slate-600 hover:border-green-400 transition"
                    >
                      <p className="font-medium text-white mb-1">
                        {product.name}
                      </p>
                      <p className="text-green-400 font-bold mb-2">
                        {product.commission} commission
                      </p>
                      <a
                        href={product.link}
                        className="text-sm text-blue-400 hover:text-blue-300 transition"
                      >
                        View Products →
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Vendor Affiliate Products Section */}
        <div className="mt-16">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-2">Vendor Affiliate Products</h2>
            <p className="text-gray-400">Curated products from community affiliates</p>
          </div>

          {/* Category Filter */}
          <div className="mb-8 flex gap-2 flex-wrap">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg transition ${
                  selectedCategory === cat
                    ? 'bg-green-600 text-white'
                    : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
                }`}
              >
                {cat}
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
              <p className="text-gray-400 mb-4">No vendor affiliate products yet</p>
              <Link href="/en/vendor/sell" className="text-green-400 hover:text-green-300">
                Be the first to upload → 
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {filteredProducts.map(product => (
                <Card key={product.id} className="bg-slate-800 border-slate-700 overflow-hidden hover:border-green-400 transition h-full flex flex-col">
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
                      <Badge className="bg-green-600 text-xs">{product.category}</Badge>
                    </div>

                    {/* Price */}
                    <div className="mb-4 flex gap-2 items-center">
                      <span className="text-xl font-bold text-green-400">₹{product.price}</span>
                      {product.original_price && (
                        <span className="text-sm text-gray-500 line-through">₹{product.original_price}</span>
                      )}
                    </div>

                    {/* Rating */}
                    {product.rating && (
                      <div className="mb-4 text-sm">
                        <span className="text-yellow-400">★ {product.rating}</span>
                        <span className="text-gray-500"> ({product.review_count || 0} reviews)</span>
                      </div>
                    )}

                    {/* Buy Button */}
                    <a
                      href={product.link || product.affiliateLink || product.affiliate_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full mt-auto px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded transition text-center text-sm"
                    >
                      View & Buy
                    </a>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* CTA Section */}
        <div className="mt-16 bg-gradient-to-r from-green-900 to-emerald-900 rounded-lg p-12 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Start Earning?
          </h2>
          <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
            Join multiple affiliate programs and start promoting products. Earn passive income by sharing products you love.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <a
              href="/marketplace"
              className="px-8 py-3 bg-white text-green-600 font-semibold rounded hover:bg-gray-100 transition"
            >
              Browse Products
            </a>
            <a
              href="/en/vendor/sell"
              className="px-8 py-3 bg-green-600 text-white font-semibold rounded hover:bg-green-700 transition flex items-center gap-2"
            >
              <ShoppingCart size={20} /> Upload Affiliate Product
            </a>
            <a
              href="/contact"
              className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded transition"
            >
              Get Help
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}
