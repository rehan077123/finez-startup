'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Sparkles } from 'lucide-react';

const decisionPaths = [
  {
    emoji: '📦',
    title: 'Start Dropshipping in 2026',
    description: 'Complete stack to launch your first store',
    setupTime: '1-2 weeks',
    difficulty: 'Beginner',
    earning: '₹10k–₹50k/month',
    roi: 'High',
  },
  {
    emoji: '🤖',
    title: 'AI Creator Monetization Stack',
    description: 'Tools to make money with AI-generated content',
    setupTime: '3-5 days',
    difficulty: 'Beginner-friendly',
    earning: '₹5k–₹25k/month',
    roi: 'Very High',
  },
  {
    emoji: '💰',
    title: 'Affiliate Marketing Mastery',
    description: 'Launch high-converting affiliate revenue',
    setupTime: '2-3 weeks',
    difficulty: 'Intermediate',
    earning: '₹3k–₹15k/month',
    roi: 'Medium',
  },
  {
    emoji: '📹',
    title: 'YouTube Automation Setup',
    description: 'Build passive income YouTube channel',
    setupTime: '1 week',
    difficulty: 'Beginner',
    earning: '₹8k–₹40k/month',
    roi: 'High',
  },
  {
    emoji: '🏠',
    title: '₹10k Home Office Setup',
    description: 'Essential gear for remote work + earning',
    setupTime: 'Same day',
    difficulty: 'Beginner',
    earning: 'Productivity focused',
    roi: 'Medium',
  },
  {
    emoji: '💪',
    title: 'Gym Transformation Starter Kit',
    description: 'Build fitness + monetize through fitness',
    setupTime: '1 week',
    difficulty: 'Beginner',
    earning: '₹2k–₹8k/month',
    roi: 'Medium',
  },
];

const categories = [
  'AI Tools',
  'Side Hustles',
  'Study & Learn',
  'Fitness',
  'Home Design',
  'Tech',
  'Fashion',
];

const testimonials = [
  {
    name: 'Alex Johnson',
    role: 'E-commerce Seller',
    text: 'The best affiliate selection I\'ve seen. High margins and real products that people actually want to buy.',
    avatar: 'https://i.pravatar.cc/150?u=alex',
  },
  {
    name: 'Sarah Chen',
    role: 'Affiliate Marketer',
    text: 'I\'ve tried many platforms, but FineZ\'s UI and product curation are top-notch. Highly recommended!',
    avatar: 'https://i.pravatar.cc/150?u=sarah',
  },
  {
    name: 'Michael Ross',
    role: 'Digital Nomad',
    text: 'FineZ helped me find my first winning dropshipping product. The insights are actual game-changers.',
    avatar: 'https://i.pravatar.cc/150?u=michael',
  },
];

const exampleQueries = [
  'best laptop for video editing under ₹50k',
  'fastest way to earn ₹20k this month',
  'AI tools to make reels + monetize',
  'dropshipping products with 60% margin',
  'side hustle for complete beginners',
  'best affiliate products in 2026',
];

export default function HomePage() {
  const [query, setQuery] = useState('');

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800/50 border border-slate-700 text-gray-300 text-sm mb-8">
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span>The Operating System for Buying & Earning Decisions</span>
          </div>
          <h1 className="text-5xl lg:text-6xl font-bold text-white mb-2 leading-tight">
            Make the Right Decision
          </h1>
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-300 mb-8">
            Not Just Find Products
          </h2>

          <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
            Too much information. Too little confidence. FineZ solves the decision gap with curated stacks, trust signals, and execution plans.
          </p>

          {/* Search Bar */}
          <div className="mb-8 max-w-3xl mx-auto">
            <div className="relative">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-yellow-400">💡</div>
              <input
                type="text"
                placeholder="best laptop for video editing under ₹50k"
                className="w-full pl-14 pr-6 py-4 rounded-lg bg-slate-800 text-white placeholder-gray-500 border border-slate-700 focus:border-yellow-400 focus:outline-none transition"
              />
            </div>
          </div>

          {/* Example Queries */}
          <div className="mb-12">
            <p className="text-gray-400 mb-4">TRY ASKING:</p>
            <div className="flex flex-wrap justify-center gap-3">
              {exampleQueries.map((query, idx) => (
                <button
                  key={idx}
                  className="text-sm text-gray-300 hover:text-yellow-400 transition px-4 py-2 rounded-full border border-gray-600 hover:border-yellow-400"
                >
                  {query}
                </button>
              ))}
            </div>
          </div>

          {/* Trust Signals */}
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-400">100K+</p>
              <p className="text-gray-400">earners</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-400">Verified</p>
              <p className="text-gray-400">Real results</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-400">Outcome-focused</p>
              <p className="text-gray-400">Plans</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-400">Action ready</p>
              <p className="text-gray-400">Stacks</p>
            </div>
          </div>
        </div>
      </div>

      {/* Popular Decision Paths */}
      <div className="border-t border-slate-800 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-white mb-4 text-center">Popular Decision Paths</h2>
          <p className="text-gray-400 text-center mb-12 max-w-2xl mx-auto">
            Choose your goal. We'll give you the complete stack + execution plan.
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {decisionPaths.map((path, idx) => (
              <div key={idx} className="bg-slate-800 border border-slate-700 rounded-lg p-6 hover:border-yellow-400 transition">
                <div className="text-4xl mb-3">{path.emoji}</div>
                <h3 className="text-lg font-bold text-white mb-2">{path.title}</h3>
                <p className="text-gray-400 text-sm mb-4">{path.description}</p>

                <div className="space-y-2 text-sm mb-4 border-t border-slate-700 pt-4">
                  <div className="flex justify-between text-gray-300">
                    <span>Setup time:</span>
                    <span className="text-yellow-400">{path.setupTime}</span>
                  </div>
                  <div className="flex justify-between text-gray-300">
                    <span>Difficulty:</span>
                    <span className="text-yellow-400">{path.difficulty}</span>
                  </div>
                  <div className="flex justify-between text-gray-300">
                    <span>Earning potential:</span>
                    <span className="text-yellow-400">{path.earning}</span>
                  </div>
                  <div className="flex justify-between text-gray-300">
                    <span>Expected ROI:</span>
                    <span className="text-yellow-400">{path.roi}</span>
                  </div>
                </div>

                <button className="w-full bg-yellow-400 hover:bg-yellow-500 text-slate-900 font-bold py-2 rounded-lg transition">
                  Explore Stack
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Testimonials */}
      <div className="border-t border-slate-800 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-white mb-12 text-center">Trusted by 10,000+ Entrepreneurs</h2>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {testimonials.map((testimonial, idx) => (
              <div key={idx} className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                <p className="text-gray-300 mb-4 italic">"{testimonial.text}"</p>
                <div className="flex items-center gap-3">
                  <img src={testimonial.avatar} alt={testimonial.name} className="w-10 h-10 rounded-full" />
                  <div>
                    <p className="text-white font-bold">{testimonial.name}</p>
                    <p className="text-gray-400 text-sm">{testimonial.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Trust Badges */}
          <div className="grid md:grid-cols-4 gap-4">
            {[
              { icon: '✓', title: 'VERIFIED TOOLS', desc: 'Hand-picked & tested' },
              { icon: '⭐', title: 'TOP RATED', desc: 'By 50k+ users' },
              { icon: '👍', title: 'EXPERT PICKS', desc: 'Daily updates' },
              { icon: '🔒', title: 'SECURE SITE', desc: 'SSL Encrypted' },
            ].map((badge, idx) => (
              <div key={idx} className="text-center p-4">
                <p className="text-2xl mb-2">{badge.icon}</p>
                <p className="text-white font-bold">{badge.title}</p>
                <p className="text-gray-400 text-sm">{badge.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900 py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="text-white font-bold mb-4">FineZ</h4>
              <p className="text-gray-400 text-sm">
                FineZ helps you discover the best tools and resources to earn money online, learn new skills, and improve your lifestyle.
              </p>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Categories</h4>
              <ul className="text-gray-400 text-sm space-y-2">
                {categories.map((cat) => (
                  <li key={cat}><Link href="#" className="hover:text-yellow-400">{cat}</Link></li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Company</h4>
              <ul className="text-gray-400 text-sm space-y-2">
                <li><Link href="/about" className="hover:text-yellow-400">About Us</Link></li>
                <li><Link href="/privacy" className="hover:text-yellow-400">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-yellow-400">Affiliate Disclaimer</Link></li>
                <li><Link href="/contact" className="hover:text-yellow-400">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Contact</h4>
              <a href="mailto:hello@finez.com" className="text-gray-400 text-sm hover:text-yellow-400">hello@finez.com</a>
            </div>
          </div>

          <div className="border-t border-slate-800 pt-8 text-center text-gray-400 text-sm">
            <p className="mb-2">© 2026 FineZ. All rights reserved.</p>
            <p>⚡ Affiliate Disclosure: This website contains affiliate links. We may earn a commission when you click on links and make a purchase, at no additional cost to you. We only recommend products we genuinely believe in.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
