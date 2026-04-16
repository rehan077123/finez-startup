"use client";

interface Spec {
  name: string;
  value: string | number;
}

interface ProductSpecsProps {
  specs: Spec[];
  title?: string;
}

export const ProductSpecs: React.FC<ProductSpecsProps> = ({
  specs,
  title = "Specifications",
}) => {
  return (
    <div>
      <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">
        {title}
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <tbody>
            {specs.map((spec, index) => (
              <tr
                key={index}
                className={`border-b border-gray-200 dark:border-slate-700 ${
                  index % 2 === 0
                    ? "bg-gray-50 dark:bg-slate-800/50"
                    : "bg-white dark:bg-slate-800"
                }`}
              >
                <td className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300 w-1/3">
                  {spec.name}
                </td>
                <td className="px-4 py-3 text-gray-600 dark:text-gray-400">
                  {spec.value}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
