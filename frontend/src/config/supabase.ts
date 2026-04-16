import { createClient } from "@supabase/supabase-js";
import { CONFIG } from "./constants";

// Helper to check if Supabase is properly configured
export const isSupabaseConfigured = () => {
  const url = CONFIG.SUPABASE_URL || "";
  return url.startsWith("http") && !!CONFIG.SUPABASE_ANON_KEY && CONFIG.SUPABASE_ANON_KEY !== "your_supabase_anon_key";
};

// Client-side Supabase client (lazy-initialized)
let supabaseClient: any = null;
export const getSupabase = () => {
  if (!supabaseClient) {
    // If not configured, use a safe dummy URL that won't crash during build
    const url = isSupabaseConfigured() ? CONFIG.SUPABASE_URL! : "https://placeholder.supabase.co";
    const key = isSupabaseConfigured() ? CONFIG.SUPABASE_ANON_KEY! : "placeholder-key";
    supabaseClient = createClient(url, key);
  }
  return supabaseClient;
};

// Server-side Supabase client (lazy-initialized)
let supabaseServerClient: any = null;
export const getSupabaseServer = () => {
  if (!supabaseServerClient) {
    // If not configured, use a safe dummy URL that won't crash during build
    const url = isSupabaseConfigured() ? CONFIG.SUPABASE_URL! : "https://placeholder.supabase.co";
    const key = process.env.SUPABASE_SERVICE_ROLE_KEY || "placeholder-key";
    supabaseServerClient = createClient(url, key, {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    });
  }
  return supabaseServerClient;
};

// REMOVED: Top-level supabase and supabaseServer constants to prevent build-time crashes.
// Use getSupabase() or getSupabaseServer() instead.
