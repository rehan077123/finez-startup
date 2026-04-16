import React, { useState } from "react";
import { ChevronDown } from "lucide-react";

interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
  defaultOpen?: string;
  allowMultiple?: boolean;
}

export const Accordion: React.FC<AccordionProps> = ({
  items,
  defaultOpen,
  allowMultiple = false,
}) => {
  const [openItems, setOpenItems] = useState<string[]>(
    defaultOpen ? [defaultOpen] : []
  );

  const toggle = (id: string) => {
    if (allowMultiple) {
      setOpenItems((prev) =>
        prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
      );
    } else {
      setOpenItems((prev) => (prev.includes(id) ? [] : [id]));
    }
  };

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <div key={item.id} className="border border-gray-200 dark:border-slate-700 rounded-lg overflow-hidden">
          <button
            onClick={() => toggle(item.id)}
            className="w-full px-4 py-3 flex justify-between items-center hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors"
          >
            <span className="font-medium text-gray-900 dark:text-white">{item.title}</span>
            <ChevronDown
              size={18}
              className={`transition-transform ${
                openItems.includes(item.id) ? "rotate-180" : ""
              }`}
            />
          </button>
          {openItems.includes(item.id) && (
            <div className="px-4 py-3 bg-gray-50 dark:bg-slate-800 border-t border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300">
              {item.content}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
