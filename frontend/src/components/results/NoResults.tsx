"use client";

import Link from "next/link";
import { Card } from "@/components/ui";
import { Search } from "lucide-react";

interface NoResultsProps {
  query?: string;
  suggestions?: string[];
  onSuggestionClick?: (suggestion: string) => void;
}

export const NoResults: React.FC<NoResultsProps> = ({
  query,
  suggestions,
  onSuggestionClick,
}) => {
  return (
    <div className="py-20 text-center">
      <Search size={48} className="mx-auto text-gray-400 mb-4" />
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        No products found
      </h2>
      {query && (
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          We couldn't find any results for "<strong>{query}</strong>"
        </p>
      )}
      <p className="text-gray-600 dark:text-gray-400 mb-8">
        Try adjusting your search or filters
      </p>

      {suggestions && suggestions.length > 0 && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-900 dark:text-white">
            Maybe you meant:
          </p>
          <div className="flex flex-wrap gap-2 justify-center">
            {suggestions.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => onSuggestionClick?.(suggestion)}
                className="px-4 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="mt-12 inline-block">
        <Link
          href="/"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Back to Home
        </Link>
      </div>
    </div>
  );
};
