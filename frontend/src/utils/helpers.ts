// Utility functions for FineZ

/**
 * Format price in INR
 */
export function formatPrice(paise: number): string {
  const rupees = paise / 100;
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 0,
  }).format(rupees);
}

/**
 * Calculate discount percentage
 */
export function calculateDiscount(
  originalPrice: number,
  currentPrice: number
): number {
  return Math.round(((originalPrice - currentPrice) / originalPrice) * 100);
}

/**
 * Generate FrieZ score based on product factors
 */
export function calculateFinezScore(
  rating: number,
  reviewCount: number,
  discountPercent: number,
  inStock: boolean
): number {
  let score = 0;
  
  // Rating component (0-40 points)
  score += (rating / 5) * 40;
  
  // Review count (0-20 points)
  const reviewScore = Math.min(reviewCount / 1000, 1) * 20;
  score += reviewScore;
  
  // Discount (0-20 points)
  score += Math.min(discountPercent / 100, 1) * 20;
  
  // Stock (20 points if available)
  score += inStock ? 20 : 0;
  
  return Math.round(score);
}

/**
 * Generate session ID
 */
export function generateSessionId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Hash IP address for privacy
 */
export function hashIP(ip: string): string {
  let hash = 0;
  for (let i = 0; i < ip.length; i++) {
    const char = ip.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash).toString(16);
}

/**
 * Generate affiliate URL
 */
export function generateAffiliateUrl(
  platform: string,
  affiliateTag: string,
  productUrl: string
): string {
  if (platform === "AMAZON") {
    const url = new URL(productUrl);
    url.searchParams.set("tag", affiliateTag);
    return url.toString();
  }
  return productUrl;
}

/**
 * Parse budget from user query
 */
export function parseBudgetFromQuery(query: string): {
  min: number | null;
  max: number | null;
} {
  const budgetMatch = query.match(/₹?(\d+k?)?[\s-]*₹?(\d+k?)?/i);
  if (!budgetMatch) return { min: null, max: null };

  const parseBudgetValue = (val: string | undefined): number | null => {
    if (!val) return null;
    const num = parseInt(val.replace("k", "000"), 10);
    return isNaN(num) ? null : num;
  };

  return {
    min: parseBudgetValue(budgetMatch[1]),
    max: parseBudgetValue(budgetMatch[2]),
  };
}

/**
 * Detect language from text
 */
export function detectLanguage(text: string): string {
  // Simple regex-based detection
  if (/[\u0900-\u097F]/.test(text)) return "hi"; // Hindi
  if (/[\u0B80-\u0BFF]/.test(text)) return "ta"; // Tamil
  if (/[\u0980-\u09FF]/.test(text)) return "bn"; // Bengali
  return "en"; // English
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, length: number): string {
  if (text.length <= length) return text;
  return text.slice(0, length) + "...";
}

/**
 * Wait for specified milliseconds
 */
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (this: any, ...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return function (this: any, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Get color based on rating
 */
export function getRatingColor(rating: number): string {
  if (rating >= 4.5) return "text-green-600";
  if (rating >= 4) return "text-lime-600";
  if (rating >= 3.5) return "text-yellow-600";
  if (rating >= 3) return "text-orange-600";
  return "text-red-600";
}

/**
 * Get platform background color
 */
export function getPlatformColor(platform: string): string {
  const colors: Record<string, string> = {
    AMAZON: "bg-orange-500",
    FLIPKART: "bg-blue-600",
    MEESHO: "bg-pink-500",
    CROMA: "bg-red-600",
    MYNTRA: "bg-orange-400",
    NYKAA: "bg-purple-500",
    AJIO: "bg-blue-500",
  };
  return colors[platform] || "bg-gray-500";
}
