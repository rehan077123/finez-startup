import { Redis } from "@upstash/redis";
import { CONFIG } from "./constants";

// Lazy-initialized Redis client
let redisClient: any = null;

export const getRedis = () => {
  if (!redisClient) {
    const url = CONFIG.REDIS_URL || "https://placeholder-redis.upstash.io";
    const token = CONFIG.REDIS_TOKEN || "placeholder-token";
    redisClient = new Redis({
      url,
      token,
    });
  }
  return redisClient;
};

// Cache helpers
export async function getCached(key: string) {
  try {
    return await getRedis().get(key);
  } catch (error) {
    console.error("Redis get error:", error);
    return null;
  }
}

export async function setCached(
  key: string,
  value: any,
  ttl: number = 3600
) {
  try {
    await getRedis().setex(key, ttl, JSON.stringify(value));
  } catch (error) {
    console.error("Redis set error:", error);
  }
}

export async function deleteCached(key: string) {
  try {
    await getRedis().del(key);
  } catch (error) {
    console.error("Redis delete error:", error);
  }
}

export async function getCachedJSON(key: string) {
  const cached = await getCached(key);
  if (!cached) return null;
  try {
    return JSON.parse(cached as string);
  } catch {
    return null;
  }
}
