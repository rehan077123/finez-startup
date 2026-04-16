import React from "react";

interface AvatarProps {
  src?: string;
  alt?: string;
  initials?: string;
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt = "Avatar",
  initials,
  size = "md",
  className,
}) => {
  const sizeClass = {
    sm: "w-8 h-8 text-xs",
    md: "w-10 h-10 text-sm",
    lg: "w-12 h-12 text-base",
    xl: "w-16 h-16 text-lg",
  };

  const colors = [
    "bg-red-500",
    "bg-blue-500",
    "bg-green-500",
    "bg-purple-500",
    "bg-yellow-500",
    "bg-pink-500",
  ];

  const colorClass = initials
    ? colors[initials.charCodeAt(0) % colors.length]
    : "bg-gray-500";

  return (
    <div
      className={`flex items-center justify-center rounded-full overflow-hidden font-semibold text-white ${sizeClass[size]} ${colorClass} ${className || ""}`}
    >
      {src ? (
        <img src={src} alt={alt} className="w-full h-full object-cover" />
      ) : (
        initials
      )}
    </div>
  );
};
