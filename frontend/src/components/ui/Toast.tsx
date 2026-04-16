import React from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error" | "info" | "warning";
  onClose: () => void;
  duration?: number;
}

export const Toast: React.FC<ToastProps> = ({
  message,
  type = "info",
  onClose,
  duration = 3000,
}) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const bgClass = {
    success: "bg-green-600",
    error: "bg-red-600",
    info: "bg-blue-600",
    warning: "bg-yellow-600",
  };

  return (
    <div
      className={`${bgClass[type]} text-white px-6 py-4 rounded-lg shadow-lg flex items-center justify-between`}
    >
      <span>{message}</span>
      <button onClick={onClose} className="ml-4 font-bold">
        ✕
      </button>
    </div>
  );
};

/* Toast Container for multiple toasts */
interface ToastContainerProps {
  toasts: Array<{ id: string; message: string; type?: "success" | "error" | "info" | "warning" }>;
  onRemove: (id: string) => void;
}

export const ToastContainer: React.FC<ToastContainerProps> = ({
  toasts,
  onRemove,
}) => (
  <div className="fixed bottom-4 right-4 space-y-2 z-max">
    {toasts.map((toast) => (
      <Toast
        key={toast.id}
        message={toast.message}
        type={toast.type}
        onClose={() => onRemove(toast.id)}
      />
    ))}
  </div>
);
