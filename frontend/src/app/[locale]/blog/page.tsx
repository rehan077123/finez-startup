'use client';

import Link from 'next/link';

export default function BlogPage() {
  const posts = [
    {
      id: 1,
      title: 'How to Find the Best Products Online',
      excerpt: 'Tips and tricks for making smart purchasing decisions',
      date: 'Apr 1, 2024',
      category: 'Guides',
    },
    {
      id: 2,
      title: 'Price Tracking: Save Money Better',
      excerpt: 'Learn how to use price alerts to catch deals',
      date: 'Mar 28, 2024',
      category: 'Money Tips',
    },
    {
      id: 3,
      title: 'Affiliate Marketing Success Stories',
      excerpt: 'How creators are earning passive income',
      date: 'Mar 25, 2024',
      category: 'Success',
    },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Navigation */}
      <nav className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-yellow-400">
              FineZ
            </Link>
            <Link href="/" className="text-white hover:text-yellow-400 transition">
              Back
            </Link>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-white mb-2">FineZ Blog</h1>
        <p className="text-gray-400 mb-12">
          Articles and guides to help you make better buying decisions
        </p>

        <div className="grid md:grid-cols-1 lg:grid-cols-2 gap-8">
          {posts.map((post) => (
            <div key={post.id} className="bg-slate-800 p-6 rounded-lg hover:bg-slate-700 transition cursor-pointer">
              <div className="flex items-center gap-2 mb-3">
                <span className="px-3 py-1 bg-yellow-400/20 text-yellow-400 rounded-full text-sm">
                  {post.category}
                </span>
                <span className="text-gray-500 text-sm">{post.date}</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">
                {post.title}
              </h3>
              <p className="text-gray-400 mb-4">
                {post.excerpt}
              </p>
              <button className="text-yellow-400 hover:text-yellow-300 transition">
                Read More →
              </button>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
