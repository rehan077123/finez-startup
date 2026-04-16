"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight, ZoomIn } from "lucide-react";
import { Modal } from "@/components/ui";

interface ProductImagesProps {
  images: string[];
  Alt: string;
}

export const ProductImages: React.FC<ProductImagesProps> = ({ images, Alt }) => {
  const [current, setCurrent] = useState(0);
  const [zoomed, setZoomed] = useState(false);

  const next = () => {
    setCurrent((prev) => (prev + 1) % images.length);
  };

  const prev = () => {
    setCurrent((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <>
      <div className="space-y-4">
        {/* Main Image */}
        <div className="relative bg-gray-100 dark:bg-slate-800 rounded-lg overflow-hidden aspect-square">
          <img
            src={images[current]}
            alt={Alt}
            className="w-full h-full object-contain"
          />

          {/* Zoom Button */}
          <button
            onClick={() => setZoomed(true)}
            className="absolute top-3 right-3 p-2 bg-white dark:bg-slate-700 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-600 transition-colors"
          >
            <ZoomIn size={18} />
          </button>

          {/* Navigation Arrows */}
          {images.length > 1 && (
            <>
              <button
                onClick={prev}
                className="absolute left-3 top-1/2 transform -translate-y-1/2 p-2 bg-white dark:bg-slate-700 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-600 transition-colors"
              >
                <ChevronLeft size={18} />
              </button>
              <button
                onClick={next}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 bg-white dark:bg-slate-700 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-600 transition-colors"
              >
                <ChevronRight size={18} />
              </button>
            </>
          )}
        </div>

        {/* Thumbnails */}
        {images.length > 1 && (
          <div className="flex gap-2 overflow-x-auto pb-2">
            {images.map((img, idx) => (
              <button
                key={idx}
                onClick={() => setCurrent(idx)}
                className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden transition-all ${
                  idx === current
                    ? "border-2 border-blue-600 ring-2 ring-blue-300 dark:ring-blue-800"
                    : "border border-gray-200 dark:border-slate-700 hover:border-gray-300 dark:hover:border-slate-600"
                }`}
              >
                <img
                  src={img}
                  alt={`${Alt}-${idx}`}
                  className="w-full h-full object-cover"
                />
              </button>
            ))}
          </div>
        )}

        {/* Counter */}
        <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
          {current + 1} / {images.length}
        </p>
      </div>

      {/* Zoom Modal */}
      <Modal isOpen={zoomed} onClose={() => setZoomed(false)}>
        <div className="w-full max-w-2xl">
          <img
            src={images[current]}
            alt={Alt}
            className="w-full h-auto rounded-lg"
          />
        </div>
      </Modal>
    </>
  );
};
