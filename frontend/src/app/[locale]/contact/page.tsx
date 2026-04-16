'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Contact form submitted:', formData);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      <nav className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
        <div className="container mx-auto px-4 py-4">
          <Link href="/" className="text-2xl font-bold text-yellow-400">
            FineZ
          </Link>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-white mb-8">Contact Us</h1>
        
        <div className="max-w-2xl">
          <form onSubmit={handleSubmit} className="bg-slate-800 p-8 rounded-lg">
            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">Name</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none"
              />
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">Email</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none"
              />
            </div>

            <div className="mb-6">
              <label className="block text-white font-semibold mb-2">Message</label>
              <textarea
                required
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-yellow-400 focus:outline-none h-32"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition"
            >
              Send Message
            </button>
          </form>

          <div className="mt-12 grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <h3 className="text-yellow-400 font-bold mb-2">Email</h3>
              <p className="text-gray-300">hello@finez.com</p>
            </div>
            <div className="text-center">
              <h3 className="text-yellow-400 font-bold mb-2">Phone</h3>
              <p className="text-gray-300">+1 (555) 123-4567</p>
            </div>
            <div className="text-center">
              <h3 className="text-yellow-400 font-bold mb-2">Address</h3>
              <p className="text-gray-300">123 Decision Street, India</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
