"use client";

import { useState, useEffect } from "react";
import { Spinner } from "@/components/ui";

interface SearchSuggestion {
  id: string;
  text: string;
  category?: string;
  searches?: number;
}

interface SearchSuggestionsProps {
  suggestions: SearchSuggestion[];
  isLoading?: boolean;
  onSelect?: (suggestion: SearchSuggestion) => void;
}

export const SearchSuggestions: React.FC<SearchSuggestionsProps> = ({
  suggestions,
  isLoading,
  onSelect,
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-6">
        <Spinner size="sm" />
      </div>
    );
  }

  if (suggestions.length === 0) {
    return null;
  }

  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
        Suggestions
      </p>
      <div className="space-y-1">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion.id}
            onClick={() => onSelect?.(suggestion)}
            className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700 dark:text-gray-300">
                {suggestion.text}
              </span>
              {suggestion.category && (
                <span className="text-xs bg-gray-200 dark:bg-slate-700 text-gray-600 dark:text-gray-400 px-2 py-1 rounded">
                  {suggestion.category}
                </span>
              )}
            </div>
            {suggestion.searches && (
              <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                {suggestion.searches.toLocaleString()} searches
              </p>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};
