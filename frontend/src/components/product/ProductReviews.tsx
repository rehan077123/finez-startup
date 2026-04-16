"use client";

import { Star, MessageCircle } from "lucide-react";
import { Card } from "@/components/ui";

interface ReviewSummary {
  pros?: string[];
  cons?: string[];
  praise?: string[];
  complaints?: string[];
  averageRating?: number;
  totalReviews?: number;
}

interface ProductReviewsProps {
  summary: ReviewSummary;
  isLoading?: boolean;
}

export const ProductReviews: React.FC<ProductReviewsProps> = ({
  summary,
  isLoading,
}) => {
  if (isLoading) {
    return <div>Loading reviews...</div>;
  }

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white">
        Customer Reviews
      </h3>

      {/* Rating Summary */}
      {summary.averageRating && (
        <Card>
          <div className="flex items-center gap-4">
            <div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-blue-600">
                  {summary.averageRating.toFixed(1)}
                </span>
                <span className="text-gray-600 dark:text-gray-400">/5</span>
              </div>
              <div className="flex items-center gap-1 mt-1">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    size={14}
                    className={
                      i < Math.floor(summary.averageRating || 0)
                        ? "fill-yellow-400 text-yellow-400"
                        : "text-gray-300"
                    }
                  />
                ))}
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                Based on {summary.totalReviews?.toLocaleString()} reviews
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* AI Summary */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Pros */}
        {summary.pros && summary.pros.length > 0 && (
          <Card className="bg-green-50 dark:bg-green-900/10 border-green-200 dark:border-green-900">
            <h4 className="font-bold text-green-900 dark:text-green-300 mb-3 flex items-center gap-2">
              <MessageCircle size={16} />
              Pros
            </h4>
            <ul className="space-y-2">
              {summary.pros.map((pro, idx) => (
                <li key={idx} className="text-sm text-green-800 dark:text-green-200 flex gap-2">
                  <span>•</span>
                  <span>{pro}</span>
                </li>
              ))}
            </ul>
          </Card>
        )}

        {/* Cons */}
        {summary.cons && summary.cons.length > 0 && (
          <Card className="bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-900">
            <h4 className="font-bold text-red-900 dark:text-red-300 mb-3 flex items-center gap-2">
              <MessageCircle size={16} />
              Cons
            </h4>
            <ul className="space-y-2">
              {summary.cons.map((con, idx) => (
                <li key={idx} className="text-sm text-red-800 dark:text-red-200 flex gap-2">
                  <span>•</span>
                  <span>{con}</span>
                </li>
              ))}
            </ul>
          </Card>
        )}
      </div>

      {/* Praise & Complaints */}
      {(summary.praise?.length || 0) > 0 && (
        <Card>
          <h4 className="font-bold text-gray-900 dark:text-white mb-2">
            What People Love
          </h4>
          <p className="text-gray-600 dark:text-gray-400">
            {summary.praise?.join(" • ")}
          </p>
        </Card>
      )}

      {(summary.complaints?.length || 0) > 0 && (
        <Card>
          <h4 className="font-bold text-gray-900 dark:text-white mb-2">
            Common Complaints
          </h4>
          <p className="text-gray-600 dark:text-gray-400">
            {summary.complaints?.join(" • ")}
          </p>
        </Card>
      )}
    </div>
  );
};
