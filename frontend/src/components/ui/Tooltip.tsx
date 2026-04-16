import React from "react";

interface TooltipProps {
  content: string;
  children: React.ReactNode;
  position?: "top" | "bottom" | "left" | "right";
}

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  position = "top",
}) => {
  const [show, setShow] = React.useState(false);

  const positionClass = {
    top: "bottom-full mb-2",
    bottom: "top-full mt-2",
    left: "right-full mr-2",
    right: "left-full ml-2",
  };

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
      >
        {children}
      </div>

      {show && (
        <div
          className={`absolute ${positionClass[position]} px-3 py-1.5 bg-gray-900 dark:bg-black text-white text-xs rounded whitespace-nowrap pointer-events-none z-50`}
        >
          {content}
          <div
            className={`absolute w-2 h-2 bg-gray-900 dark:bg-black ${
              position === "top"
                ? "bottom-[-4px] left-1/2 transform -translate-x-1/2 rotate-45"
                : position === "bottom"
                ? "top-[-4px] left-1/2 transform -translate-x-1/2 rotate-45"
                : position === "left"
                ? "right-[-4px] top-1/2 transform -translate-y-1/2 rotate-45"
                : "left-[-4px] top-1/2 transform -translate-y-1/2 rotate-45"
            }`}
          />
        </div>
      )}
    </div>
  );
};
