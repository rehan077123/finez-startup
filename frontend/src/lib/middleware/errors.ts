// Error handling middleware
import { NextRequest, NextResponse } from "next/server";

export class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string
  ) {
    super(message);
    this.name = "AppError";
  }
}

export interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code?: string;
    status: number;
    timestamp: string;
  };
}

/**
 * Handle API errors
 */
export function handleError(error: any): NextResponse<ErrorResponse> {
  console.error("API Error:", error);

  if (error instanceof AppError) {
    return NextResponse.json(
      {
        success: false,
        error: {
          message: error.message,
          code: error.code,
          status: error.statusCode,
          timestamp: new Date().toISOString(),
        },
      },
      { status: error.statusCode }
    );
  }

  if (error instanceof SyntaxError) {
    return NextResponse.json(
      {
        success: false,
        error: {
          message: "Invalid request body",
          code: "INVALID_JSON",
          status: 400,
          timestamp: new Date().toISOString(),
        },
      },
      { status: 400 }
    );
  }

  // Default error response
  return NextResponse.json(
    {
      success: false,
      error: {
        message: "Internal server error",
        code: "INTERNAL_ERROR",
        status: 500,
        timestamp: new Date().toISOString(),
      },
    },
    { status: 500 }
  );
}

/**
 * Wrap API handler with error handling
 */
export function withErrorHandling(
  handler: (req: NextRequest) => Promise<NextResponse>
) {
  return async (req: NextRequest) => {
    try {
      return await handler(req);
    } catch (error) {
      return handleError(error);
    }
  };
}

export default {
  AppError,
  handleError,
  withErrorHandling,
};
