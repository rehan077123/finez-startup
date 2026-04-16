import React from "react";
import Link from "next/link";
import { ChevronRight } from "lucide-react";

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({ items }) => {
  return (
    <nav className="flex items-center space-x-2 text-sm">
      {items.map((item, index) => (
        <React.Fragment key={index}>
          {index > 0 && <ChevronRight size={16} className="text-gray-400" />}
          {item.href ? (
            <Link
              href={item.href}
              className="text-blue-600 hover:underline dark:text-blue-400"
            >
              {item.label}
            </Link>
          ) : (
            <span className="text-gray-600 dark:text-gray-400">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
};
