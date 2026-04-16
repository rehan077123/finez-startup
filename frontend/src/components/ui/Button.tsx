import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  children: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", isLoading, className, ...props }, ref) => {
    const baseClass =
      "font-semibold rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed";

    const variantClass = {
      primary: "bg-blue-600 text-white hover:bg-blue-700",
      secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-slate-700 dark:text-white dark:hover:bg-slate-600",
      outline:
        "border-2 border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-slate-800",
      ghost: "hover:bg-gray-100 dark:hover:bg-slate-800",
      danger: "bg-red-600 text-white hover:bg-red-700",
    };

    const sizeClass = {
      sm: "px-3 py-2 text-sm",
      md: "px-4 py-2.5 text-base",
      lg: "px-6 py-3 text-lg",
    };

    return (
      <button
        ref={ref}
        className={`${baseClass} ${variantClass[variant]} ${sizeClass[size]} ${className || ""}`}
        disabled={isLoading || props.disabled}
        {...props}
      >
        {isLoading && <span className="animate-spin">⚙️</span>}
        {props.children}
      </button>
    );
  }
);

Button.displayName = "Button";
