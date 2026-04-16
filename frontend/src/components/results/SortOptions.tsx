"use client";

import { Select, Button } from "@/components/ui";
import { ArrowUpDown } from "lucide-react";

type SortOption = "relevance" | "price-asc" | "price-desc" | "rating" | "newest";

interface SortOptionsProps {
  value?: SortOption;
  onChange?: (option: SortOption) => void;
}

export const SortOptions: React.FC<SortOptionsProps> = ({ value, onChange }) => {
  const sortOptions = [
    { value: "relevance", label: "Most Relevant" },
    { value: "price-asc", label: "Price: Low to High" },
    { value: "price-desc", label: "Price: High to Low" },
    { value: "rating", label: "Highest Rated" },
    { value: "newest", label: "Newest" },
  ];

  return (
    <div className="flex items-center gap-2">
      <ArrowUpDown size={16} className="text-gray-600 dark:text-gray-400" />
      <select
        value={value || "relevance"}
        onChange={(e) => onChange?.(e.target.value as SortOption)}
        className="px-3 py-2 border border-gray-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {sortOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};
