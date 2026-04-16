// CORS middleware
import { NextRequest, NextResponse } from "next/server";

export interface CORSOptions {
  origin?: string | string[] | boolean;
  methods?: string[];
  allowedHeaders?: string[];
  exposedHeaders?: string[];
  credentials?: boolean;
  maxAge?: number;
}

/**
 * Apply CORS headers to response
 */
export function applyCORS(
  response: NextResponse,
  options: CORSOptions = {}
) {
  const {
    origin = true,
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH"],
    allowedHeaders = ["Content-Type", "Authorization"],
    exposedHeaders = ["Content-Length"],
    credentials = true,
    maxAge = 86400,
  } = options;

  if (origin === true) {
    response.headers.set("Access-Control-Allow-Origin", "*");
  } else if (typeof origin === "string") {
    response.headers.set("Access-Control-Allow-Origin", origin);
  } else if (Array.isArray(origin)) {
    response.headers.set(
      "Access-Control-Allow-Origin",
      origin.join(",")
    );
  }

  response.headers.set("Access-Control-Allow-Methods", methods.join(","));
  response.headers.set(
    "Access-Control-Allow-Headers",
    allowedHeaders.join(",")
  );
  response.headers.set(
    "Access-Control-Expose-Headers",
    exposedHeaders.join(",")
  );

  if (credentials) {
    response.headers.set("Access-Control-Allow-Credentials", "true");
  }

  response.headers.set("Access-Control-Max-Age", maxAge.toString());

  return response;
}

/**
 * Handle CORS preflight requests
 */
export function handleCORSPreflight(
  request: NextRequest,
  options?: CORSOptions
) {
  if (request.method === "OPTIONS") {
    const response = new NextResponse(null, { status: 204 });
    return applyCORS(response, options);
  }

  return null;
}

export default {
  applyCORS,
  handleCORSPreflight,
};
