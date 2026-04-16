import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hoverable?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  hoverable = false,
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className={`bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 p-6 ${
        hoverable ? "hover:shadow-lg transition-shadow cursor-pointer" : ""
      } ${className || ""}`}
    >
      {children}
    </div>
  );
};
