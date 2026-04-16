import React from "react";

interface ProgressProps {
  value: number;
  max?: number;
  size?: "sm" | "md" | "lg";
  color?: "primary" | "success" | "warning" | "error";
  label?: string;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  max = 100,
  size = "md",
  color = "primary",
  label,
}) => {
  const percentage = (value / max) * 100;

  const heightClass = {
    sm: "h-1",
    md: "h-2",
    lg: "h-3",
  };

  const colorClass = {
    primary: "bg-blue-600",
    success: "bg-green-600",
    warning: "bg-yellow-600",
    error: "bg-red-600",
  };

  return (
    <div>
      {label && (
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium">{label}</span>
          <span className="text-sm text-gray-600 dark:text-gray-400">
            {Math.round(percentage)}%
          </span>
        </div>
      )}
      <div className={`w-full bg-gray-200 dark:bg-slate-700 rounded-full overflow-hidden ${heightClass[size]}`}>
        <div
          className={`${colorClass[color]} h-full transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
