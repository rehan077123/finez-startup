'use client';

import Link from 'next/link';

export default function AboutPage() {
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
        <h1 className="text-4xl font-bold text-white mb-6">About FineZ</h1>

        <div className="max-w-3xl">
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-yellow-400 mb-4">Our Mission</h2>
            <p className="text-gray-300 mb-4">
              We believe that making a purchase decision shouldn't be a painful process. That's why we built FineZ - 
              the operating system for buying and earning decisions.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-yellow-400 mb-4">What We Do</h2>
            <p className="text-gray-300 mb-4">
              FineZ helps you:
            </p>
            <ul className="text-gray-300 space-y-2 ml-6">
              <li>✓ Discover products that match your lifestyle</li>
              <li>✓ Compare prices across multiple platforms</li>
              <li>✓ Get AI-powered buying guides</li>
              <li>✓ Track price changes and catch deals</li>
              <li>✓ Earn money through affiliate marketing</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-yellow-400 mb-4">Our Team</h2>
            <p className="text-gray-300">
              Built by a team of product enthusiasts and engineers who believe technology 
              should make decision-making easier, not harder.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-4">Contact Us</h2>
            <p className="text-gray-300">
              Questions? Reach out to us at hello@finez.com
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}
