"use client";

import { Badge, Button } from "@/components/ui";
import { X } from "lucide-react";

interface SearchFilter {
  id: string;
  label: string;
  value: string;
}

interface SearchFiltersProps {
  filters: SearchFilter[];
  activeFilters: string[];
  onToggle?: (filterId: string) => void;
  onClear?: () => void;
  title?: string;
}

export const SearchFilters: React.FC<SearchFiltersProps> = ({
  filters,
  activeFilters,
  onToggle,
  onClear,
  title = "Filters",
}) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-gray-900 dark:text-white">{title}</h3>
        {activeFilters.length > 0 && (
          <button
            onClick={onClear}
            className="text-sm text-blue-600 hover:underline dark:text-blue-400"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {filters.map((filter) => {
          const isActive = activeFilters.includes(filter.id);
          return (
            <button
              key={filter.id}
              onClick={() => onToggle?.(filter.id)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-slate-600"
              }`}
            >
              {filter.label}
              {isActive && <X size={14} />}
            </button>
          );
        })}
      </div>
    </div>
  );
};
