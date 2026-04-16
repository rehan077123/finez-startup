'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Card, Badge } from '@/components/ui';
import { Lightbulb, Users, TrendingUp, Zap } from 'lucide-react';

const STACKS = [
  {
    id: 1,
    title: 'Professional Productivity Stack',
    description: 'Complete setup for remote workers & professionals',
    icon: '💼',
    products: [
      { name: 'MacBook Pro 14 M3', price: '₹139,999', link: 'https://amazon.in/s?k=MacBook+Pro' },
      { name: 'Del Monitor 24"', price: '₹22,999', link: 'https://amazon.in/s?k=Dell+Monitor' },
      { name: 'Corsair Keyboard', price: '₹12,999', link: 'https://amazon.in/s?k=Mechanical+Keyboard' },
      { name: 'Logitech MX Mouse', price: '₹8,999', link: 'https://amazon.in/s?k=Logitech+Mouse' },
    ],
    totalCost: '₹184,996',
    uses: ['Remote Work', 'Content Creation', 'Coding', 'Design'],
    benefits: ['High Performance', 'Ultra-Wide Display', 'Ergonomic', 'Wireless Freedom'],
  },
  {
    id: 2,
    title: 'Mobile-First Tech Stack',
    description: 'Latest smartphones & accessories for mobile enthusiasts',
    icon: '📱',
    products: [
      { name: 'Samsung Galaxy S24 Ultra', price: '₹129,999', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24' },
      { name: 'Apple AirPods Pro', price: '₹24,999', link: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY' },
      { name: 'Apple Watch Series 9', price: '₹41,999', link: 'https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D' },
    ],
    totalCost: '₹196,997',
    uses: ['Mobile Photography', 'Fitness Tracking', 'Music Listening', 'Smart Life'],
    benefits: ['Best Camera', 'Seamless Integration', 'All-Day Battery', 'Premium Build'],
  },
  {
    id: 3,
    title: 'Gaming & Entertainment',
    description: 'Ultimate setup for gamers & content consumers',
    icon: '🎮',
    products: [
      { name: 'Samsung Galaxy S24 Ultra', price: '₹129,999', link: '#' },
      { name: 'Dell P2423D Monitor', price: '₹22,999', link: '#' },
      { name: 'Corsair Keyboard', price: '₹12,999', link: '#' },
      { name: 'Apple AirPods Pro', price: '₹24,999', link: '#' },
    ],
    totalCost: '₹190,996',
    uses: ['Gaming', 'Movie Watching', 'Music Production', 'Streaming'],
    benefits: ['120Hz Display', 'Spatial Audio', 'Mechanical Switches', 'Low Latency'],
  },
];

export default function IdeasPage() {
  const [selectedStack, setSelectedStack] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <div className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center gap-3 mb-2">
            <Lightbulb className="text-yellow-400" size={32} />
            <h1 className="text-4xl font-bold text-white">Product Ideas & Stacks</h1>
          </div>
          <p className="text-gray-400 ml-11">Curated product bundles for different use cases</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <TrendingUp className="mx-auto text-blue-400 mb-3" size={32} />
            <div className="text-3xl font-bold text-white">{STACKS.length}</div>
            <p className="text-gray-400 text-sm mt-1">Curated Stacks</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <Users className="mx-auto text-green-400 mb-3" size={32} />
            <div className="text-3xl font-bold text-white">10K+</div>
            <p className="text-gray-400 text-sm mt-1">Users Following</p>
          </Card>
          <Card className="p-6 bg-slate-800 border-slate-700 text-center">
            <Zap className="mx-auto text-yellow-400 mb-3" size={32} />
            <div className="text-3xl font-bold text-white">₹100K+</div>
            <p className="text-gray-400 text-sm mt-1">Total Budget Range</p>
          </Card>
        </div>

        {/* Stacks Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {STACKS.map(stack => (
            <Card
              key={stack.id}
              className="bg-slate-800 border-slate-700 overflow-hidden hover:border-yellow-400 transition cursor-pointer"
              onClick={() => setSelectedStack(selectedStack === stack.id ? null : stack.id)}
            >
              <div className="p-6">
                <div className="text-5xl mb-3">{stack.icon}</div>
                <h3 className="text-xl font-bold text-white mb-1">{stack.title}</h3>
                <p className="text-gray-400 text-sm mb-4">{stack.description}</p>

                <div className="bg-slate-700 rounded-lg p-3 mb-4">
                  <p className="text-xs text-gray-400">Total Investment</p>
                  <p className="text-2xl font-bold text-yellow-400">{stack.totalCost}</p>
                </div>

                <div className="flex flex-wrap gap-2 mb-4">
                  {stack.uses.map(use => (
                    <Badge key={use} className="bg-blue-600 text-xs">
                      {use}
                    </Badge>
                  ))}
                </div>

                <button
                  onClick={() => setSelectedStack(selectedStack === stack.id ? null : stack.id)}
                  className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition"
                >
                  {selectedStack === stack.id ? 'Hide Details' : 'Explore Stack'}
                </button>

                {/* Expanded Details */}
                {selectedStack === stack.id && (
                  <div className="mt-6 pt-6 border-t border-slate-700">
                    <h4 className="font-semibold text-white mb-3">Products in this stack:</h4>
                    <div className="space-y-2 mb-4">
                      {stack.products.map((product, idx) => (
                        <div key={idx} className="flex justify-between items-center bg-slate-700 p-3 rounded">
                          <div>
                            <p className="text-white text-sm font-medium">{product.name}</p>
                            <p className="text-yellow-400 text-sm">{product.price}</p>
                          </div>
                          <a
                            href={product.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-3 py-1 bg-yellow-600 hover:bg-yellow-700 text-white text-xs rounded transition"
                          >
                            View
                          </a>
                        </div>
                      ))}
                    </div>

                    <h4 className="font-semibold text-white mb-2 mt-4">Benefits:</h4>
                    <ul className="space-y-1">
                      {stack.benefits.map((benefit, idx) => (
                        <li key={idx} className="text-gray-300 text-sm flex items-center">
                          <span className="text-green-400 mr-2">✓</span>
                          {benefit}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
