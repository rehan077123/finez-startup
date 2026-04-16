import React from "react";

interface DividerProps {
  orientation?: "horizontal" | "vertical";
  className?: string;
  label?: string;
}

export const Divider: React.FC<DividerProps> = ({
  orientation = "horizontal",
  className,
  label,
}) => {
  if (orientation === "vertical") {
    return (
      <div
        className={`h-full w-0.5 bg-gray-200 dark:bg-slate-700 ${className || ""}`}
      />
    );
  }

  if (label) {
    return (
      <div className={`flex items-center ${className || ""}`}>
        <div className="flex-1 border-t border-gray-200 dark:border-slate-700" />
        <span className="px-4 text-sm text-gray-500 dark:text-gray-400">
          {label}
        </span>
        <div className="flex-1 border-t border-gray-200 dark:border-slate-700" />
      </div>
    );
  }

  return (
    <div className={`border-t border-gray-200 dark:border-slate-700 ${className || ""}`} />
  );
};
