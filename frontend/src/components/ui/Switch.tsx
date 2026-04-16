import React from "react";

interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}

export const Switch = React.forwardRef<HTMLInputElement, SwitchProps>(
  ({ label, className, ...props }, ref) => {
    return (
      <div className="flex items-center">
        <label className="flex items-center cursor-pointer">
          <input
            ref={ref}
            type="checkbox"
            className="peer hidden"
            {...props}
          />
          <div className="relative w-11 h-6 bg-gray-300 rounded-full transition-colors peer-checked:bg-blue-600 dark:bg-slate-600 dark:peer-checked:bg-blue-500">
            <div className="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full transition-transform peer-checked:translate-x-5" />
          </div>
          {label && <span className="ml-3 text-sm font-medium">{label}</span>}
        </label>
      </div>
    );
  }
);

Switch.displayName = "Switch";
