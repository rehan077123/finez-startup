"use client";

import { useEffect, useState } from "react";
import { Clock, X } from "lucide-react";

interface SearchHistoryProps {
  maxItems?: number;
  onSelect?: (query: string) => void;
  onDelete?: (query: string) => void;
}

export const SearchHistory: React.FC<SearchHistoryProps> = ({
  maxItems = 5,
  onSelect,
  onDelete,
}) => {
  const [history, setHistory] = useState<string[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem("searchHistory");
    if (stored) {
      setHistory(JSON.parse(stored).slice(0, maxItems));
    }
  }, [maxItems]);

  const handleDelete = (query: string) => {
    setHistory((prev) => prev.filter((h) => h !== query));
    const stored = localStorage.getItem("searchHistory");
    if (stored) {
      const updated = JSON.parse(stored).filter((q: string) => q !== query);
      localStorage.setItem("searchHistory", JSON.stringify(updated));
    }
    onDelete?.(query);
  };

  if (history.length === 0) {
    return null;
  }

  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
        Recent Searches
      </p>
      <div className="space-y-1">
        {history.map((query) => (
          <button
            key={query}
            onClick={() => onSelect?.(query)}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors text-left"
          >
            <Clock size={14} />
            <span className="flex-1 truncate text-sm">{query}</span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDelete(query);
              }}
              className="hover:text-red-600 dark:hover:text-red-400"
            >
              <X size={14} />
            </button>
          </button>
        ))}
      </div>
    </div>
  );
};
