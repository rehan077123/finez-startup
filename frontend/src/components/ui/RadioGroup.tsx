import React from "react";

interface RadioOption {
  value: string;
  label: string;
  description?: string;
}

interface RadioGroupProps {
  name: string;
  options: RadioOption[];
  value?: string;
  onChange?: (value: string) => void;
  label?: string;
  error?: string;
}

export const RadioGroup = React.forwardRef<HTMLDivElement, RadioGroupProps>(
  ({ name, options, value, onChange, label, error }, ref) => {
    return (
      <div ref={ref} className="w-full">
        {label && (
          <label className="block text-sm font-medium mb-3 text-gray-700 dark:text-gray-300">
            {label}
          </label>
        )}
        <div className={`space-y-2 p-2 rounded-lg ${error ? "bg-red-50 dark:bg-red-900/10" : ""}`}>
          {options.map((option) => (
            <label
              key={option.value}
              className="flex items-start p-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
            >
              <input
                type="radio"
                name={name}
                value={option.value}
                checked={value === option.value}
                onChange={(e) => onChange?.(e.target.value)}
                className="mt-1 w-4 h-4"
              />
              <div className="ml-3">
                <span className="font-medium text-gray-900 dark:text-white block">
                  {option.label}
                </span>
                {option.description && (
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {option.description}
                  </span>
                )}
              </div>
            </label>
          ))}
        </div>
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
      </div>
    );
  }
);

RadioGroup.displayName = "RadioGroup";
