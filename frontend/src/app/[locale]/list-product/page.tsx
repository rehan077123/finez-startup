'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function ListProductPage() {
  const [formData, setFormData] = useState({
    productName: '',
    description: '',
    price: '',
    category: '',
    image: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle product listing submission
    console.log('Product listing submitted:', formData);
  };

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
        <h1 className="text-4xl font-bold text-white mb-2">List Your Product</h1>
        <p className="text-gray-400 mb-8">
          Share your product with thousands of buyers on FineZ
        </p>

        <div className="max-w-2xl">
          <form onSubmit={handleSubmit} className="bg-slate-800 p-8 rounded-lg">
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                Product Name
              </label>
              <input
                type="text"
                required
                value={formData.productName}
                onChange={(e) =>
                  setFormData({ ...formData, productName: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none"
              />
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                Description
              </label>
              <textarea
                required
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none h-24"
              />
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                Price (₹)
              </label>
              <input
                type="number"
                required
                value={formData.price}
                onChange={(e) =>
                  setFormData({ ...formData, price: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none"
              />
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                Category
              </label>
              <select
                value={formData.category}
                onChange={(e) =>
                  setFormData({ ...formData, category: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none"
              >
                <option value="">Select Category</option>
                <option value="Electronics">Electronics</option>
                <option value="Fashion">Fashion</option>
                <option value="Home">Home & Living</option>
                <option value="Sports">Sports</option>
                <option value="Books">Books</option>
              </select>
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">
                Product Image URL
              </label>
              <input
                type="url"
                value={formData.image}
                onChange={(e) =>
                  setFormData({ ...formData, image: e.target.value })
                }
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition"
            >
              List Product
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
