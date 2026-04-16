import React from "react";

interface SkeletonProps {
  className?: string;
  count?: number;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className = "w-full h-4",
  count = 1,
}) => {
  return (
    <div className="space-y-2">
      {[...Array(count)].map((_, i) => (
        <div
          key={i}
          className={`bg-gradient-to-r from-gray-200 to-gray-300 dark:from-slate-700 dark:to-slate-600 animate-pulse rounded ${className}`}
        />
      ))}
    </div>
  );
};

export const CardSkeleton: React.FC = () => (
  <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 p-6">
    <Skeleton className="w-48 h-6 mb-4" />
    <Skeleton className="w-full h-4 mb-3" count={3} />
    <Skeleton className="w-32 h-8 mt-4" />
  </div>
);
