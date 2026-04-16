'use client';

import Link from 'next/link';

export default function TermsPage() {
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
        <h1 className="text-4xl font-bold text-white mb-8">Terms of Service</h1>
        <div className="max-w-3xl text-gray-300 space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-2">License</h2>
            <p>Unless otherwise stated, FineZ owns the intellectual property rights for all material on this website.</p>
          </section>
          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-2">User Responsibilities</h2>
            <p>Users are responsible for maintaining the confidentiality of their account information.</p>
          </section>
          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-2">Limitations of Liability</h2>
            <p>FineZ shall not be liable for any damages arising out of or in connection with your use of this website.</p>
          </section>
        </div>
      </div>
    </main>
  );
}
