"use client";

import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-12 mt-20">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Company */}
          <div>
            <h3 className="font-bold text-white mb-4">FineZ</h3>
            <p className="text-sm mb-4">
              AI-powered product discovery and comparison for India.
            </p>
            <div className="flex gap-4">
              <Link href="/" className="text-gray-400 hover:text-white">
                Twitter
              </Link>
              <Link href="/" className="text-gray-400 hover:text-white">
                Instagram
              </Link>
            </div>
          </div>

          {/* Product */}
          <div>
            <h4 className="font-semibold text-white mb-4">Product</h4>
            <Link href="/search" className="block text-sm mb-2 hover:text-white">
              Search
            </Link>
            <Link href="/deals" className="block text-sm mb-2 hover:text-white">
              Deals
            </Link>
            <Link href="/guides" className="block text-sm mb-2 hover:text-white">
              Guides
            </Link>
            <Link href="/compare" className="block text-sm mb-2 hover:text-white">
              Compare
            </Link>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-semibold text-white mb-4">Company</h4>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              About
            </Link>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              Blog
            </Link>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              Careers
            </Link>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              Contact
            </Link>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold text-white mb-4">Legal</h4>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              Privacy
            </Link>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              Terms
            </Link>
            <Link href="/" className="block text-sm mb-2 hover:text-white">
              Cookies
            </Link>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-sm text-center">
          <p>
            © 2024 FineZ. All rights reserved. | India&apos;s #1 AI Shopping
            Assistant
          </p>
        </div>
      </div>
    </footer>
  );
}
