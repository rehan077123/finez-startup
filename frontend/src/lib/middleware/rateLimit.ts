// Rate limiting middleware
// Install: npm install redis

import { Redis } from "@upstash/redis";

// Lazy-initialized Redis client for rate limiting
let redisClient: any = null;

const getRedis = () => {
  if (!redisClient) {
    const url = process.env.REDIS_URL || "https://placeholder-redis.upstash.io";
    const token = process.env.REDIS_TOKEN || "placeholder-token";
    redisClient = new Redis({
      url,
      token,
    });
  }
  return redisClient;
};

interface RateLimitConfig {
  interval: number; // Time window in seconds
  maxRequests: number; // Max requests in interval
}

/**
 * Rate limit middleware
 */
export async function rateLimit(
  identifier: string,
  config: RateLimitConfig = { interval: 60, maxRequests: 100 }
) {
  try {
    const redis = getRedis();
    const key = `rate-limit:${identifier}`;
    const current = await redis.incr(key);

    if (current === 1) {
      // First request in the window
      await redis.expire(key, config.interval);
    }

    return {
      allowed: current <= config.maxRequests,
      remaining: Math.max(0, config.maxRequests - current),
      resetIn: await redis.ttl(key),
    };
  } catch (error) {
    console.error("Rate limit check failed:", error);
    // Allow request if rate limit check fails
    return {
      allowed: true,
      remaining: config.maxRequests,
      resetIn: config.interval,
    };
  }
}

/**
 * Sliding window rate limiter
 */
export async function slidingWindowRateLimit(
  identifier: string,
  config: RateLimitConfig = { interval: 60, maxRequests: 100 }
) {
  try {
    const redis = getRedis();
    const key = `rate-limit:sliding:${identifier}`;
    const now = Date.now();
    const windowStart = now - config.interval * 1000;

    // Remove old entries
    await redis.zremrangebyscore(
      key,
      "-inf",
      windowStart
    );

    // Count requests in current window
    const count = await redis.zcard(key);

    if (count < config.maxRequests) {
      // Add current request
      await redis.zadd(key, { score: now, member: `${now}-${Math.random()}` });
      await redis.expire(key, config.interval);
      return {
        allowed: true,
        remaining: config.maxRequests - count - 1,
        resetIn: config.interval,
      };
    }

    return {
      allowed: false,
      remaining: 0,
      resetIn: config.interval,
    };
  } catch (error) {
    console.error("Sliding window rate limit check failed:", error);
    return {
      allowed: true,
      remaining: config.maxRequests,
      resetIn: config.interval,
    };
  }
}

export default {
  rateLimit,
  slidingWindowRateLimit,
};
