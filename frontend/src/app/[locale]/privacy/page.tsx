'use client';

import Link from 'next/link';

export default function PrivacyPage() {
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
        <h1 className="text-4xl font-bold text-white mb-8">Privacy Policy</h1>
        <div className="max-w-3xl text-gray-300 space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-2">Introduction</h2>
            <p>Your privacy is important to us. This privacy policy explains how we collect, use, and protect your information.</p>
          </section>
          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-2">Data Collection</h2>
            <p>We collect information you provide directly to us, such as when you create an account or make a purchase.</p>
          </section>
          <section>
            <h2 className="text-2xl font-bold text-yellow-400 mb-2">How We Use Data</h2>
            <p>We use your data to provide, improve, and personalize our services.</p>
          </section>
        </div>
      </div>
    </main>
  );
}
