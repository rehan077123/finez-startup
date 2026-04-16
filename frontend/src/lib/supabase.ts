import { createClient } from '@supabase/supabase-js';

// Lazy-initialized clients
let supabaseClient: any = null;
let supabaseServerClient: any = null;

// Client-side Supabase client (lazy function)
export const getSupabase = () => {
  if (!supabaseClient) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
    const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key';
    supabaseClient = createClient(url, key);
  }
  return supabaseClient;
};

// Server-side Supabase client (lazy function)
export const getServerSupabase = () => {
  if (!supabaseServerClient) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
    const key = process.env.SUPABASE_SERVICE_ROLE_KEY || 'placeholder-key';
    
    supabaseServerClient = createClient(url, key, {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    });
  }
  return supabaseServerClient;
};
