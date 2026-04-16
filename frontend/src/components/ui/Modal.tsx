import React from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg";
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
}) => {
  if (!isOpen) return null;

  const sizeClass = {
    sm: "max-w-sm",
    md: "max-w-md",
    lg: "max-w-lg",
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className={`bg-white dark:bg-slate-800 rounded-lg shadow-lg max-h-[90vh] overflow-y-auto ${sizeClass[size]}`}
          onClick={(e) => e.stopPropagation()}
        >
          {title && (
            <div className="border-b border-gray-200 dark:border-slate-700 px-6 py-4">
              <h2 className="text-xl font-bold">{title}</h2>
            </div>
          )}
          <div className="p-6">{children}</div>
        </div>
      </div>
    </>
  );
};
