import React from "react";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: "primary" | "secondary";
  className?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = "md",
  color = "primary",
  className,
}) => {
  const sizeClass = {
    sm: "w-4 h-4",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };

  const colorClass = {
    primary: "border-blue-600",
    secondary: "border-gray-400",
  };

  return (
    <div
      className={`border-4 border-transparent rounded-full animate-spin ${sizeClass[size]} ${colorClass[color]} ${className || ""}`}
      style={{
        borderTopColor: color === "primary" ? "#2563eb" : "#9ca3af",
      }}
    />
  );
};
