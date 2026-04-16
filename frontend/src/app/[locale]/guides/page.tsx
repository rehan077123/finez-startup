"use client";

import { useState, useEffect } from "react";
import { Card, Button, Badge, Spinner } from "@/components/ui";
import { BookOpen, Share2, ThumbsUp } from "lucide-react";

interface Guide {
  id: string;
  title: string;
  excerpt: string;
  category: string;
  author: string;
  readTime: number;
  likes: number;
  publishedAt: string;
  image: string;
}

export default function GuidesPage() {
  const [guides, setGuides] = useState<Guide[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setGuides([
      {
        id: "1",
        title: "How to Find Best Deals Online",
        excerpt:
          "Learn expert tricks to save money on every purchase. Discover timing strategies, cashback tricks, and more.",
        category: "Shopping Tips",
        author: "Expert Team",
        readTime: 5,
        likes: 234,
        publishedAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
        image: "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=500&h=500&fit=crop",
      },
      {
        id: "2",
        title: "Complete Buyer's Guide to Smartphones",
        excerpt:
          "Everything you need to know before buying your next smartphone. Compare specs, prices, and brands.",
        category: "Buyer's Guide",
        author: "Tech Experts",
        readTime: 12,
        likes: 567,
        publishedAt: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString(),
        image: "https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg",
      },
    ]);
    setIsLoading(false);
  }, []);

  if (isLoading) return <Spinner size="lg" />;

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white flex items-center gap-3 mb-2">
          <BookOpen size={36} />
          Guides & Tips
        </h1>
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          Expert advice to help you shop smarter
        </p>
      </div>

      <div className="space-y-6">
        {guides.map((guide) => (
          <Card key={guide.id} className="overflow-hidden hover:shadow-lg transition-shadow">
            <div className="grid md:grid-cols-3 gap-6 p-6">
              <div className="flex items-center justify-center bg-gray-100 dark:bg-slate-700 h-40 rounded-lg overflow-hidden">
                <img
                  src={guide.image}
                  alt={guide.title}
                  className="w-full h-40 object-cover rounded-lg"
                />
              </div>
              <div className="md:col-span-2">
                <div className="flex items-start justify-between mb-2">
                  <Badge variant="secondary">{guide.category}</Badge>
                  <span className="text-sm text-gray-500">
                    {guide.readTime} min read
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                  {guide.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  {guide.excerpt}
                </p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    <span>By {guide.author}</span>
                    <span>
                      {new Date(guide.publishedAt).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      <ThumbsUp size={16} className="mr-1" />
                      {guide.likes}
                    </Button>
                    <Button size="sm" variant="outline">
                      <Share2 size={16} />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="mt-12 text-center">
        <Button size="lg">Load More Guides</Button>
      </div>
    </div>
  );
}
