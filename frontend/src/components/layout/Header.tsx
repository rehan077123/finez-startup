"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, Search, Bell, User, ShoppingCart } from "lucide-react";

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-slate-900 dark:border-slate-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">F</span>
            </div>
            <span className="hidden sm:inline font-bold text-xl">FineZ</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/search" className="text-gray-700 dark:text-gray-300 hover:text-blue-600">
              Search
            </Link>
            <Link href="/deals" className="text-gray-700 dark:text-gray-300 hover:text-blue-600">
              Deals
            </Link>
            <Link href="/guides" className="text-gray-700 dark:text-gray-300 hover:text-blue-600">
              Guides
            </Link>
            <Link href="/pro" className="text-gray-700 dark:text-gray-300 hover:text-blue-600">
              Pro
            </Link>
          </nav>

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg">
              <Search size={20} />
            </button>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg">
              <Bell size={20} />
            </button>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg">
              <ShoppingCart size={20} />
            </button>
            <Link href="/profile">
              <button className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg">
                <User size={20} />
              </button>
            </Link>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2"
            >
              {mobileOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileOpen && (
          <div className="md:hidden pb-4 border-t">
            <Link href="/search" className="block py-2 text-gray-700 dark:text-gray-300">
              Search
            </Link>
            <Link href="/deals" className="block py-2 text-gray-700 dark:text-gray-300">
              Deals
            </Link>
            <Link href="/guides" className="block py-2 text-gray-700 dark:text-gray-300">
              Guides
            </Link>
            <Link href="/pro" className="block py-2 text-gray-700 dark:text-gray-300">
              Pro
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
