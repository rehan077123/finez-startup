// Validation middleware
import { NextRequest, NextResponse } from "next/server";

export type ValidationRule = {
  required?: boolean;
  type?: "string" | "number" | "boolean" | "email" | "url";
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean | string;
};

export type ValidationSchema = Record<string, ValidationRule>;

export interface ValidationError {
  field: string;
  message: string;
}

/**
 * Validate request body against schema
 */
export function validateRequest(
  data: any,
  schema: ValidationSchema
): { valid: boolean; errors: ValidationError[] } {
  const errors: ValidationError[] = [];

  for (const [field, rule] of Object.entries(schema)) {
    const value = data[field];

    // Check required
    if (rule.required && (value === null || value === undefined || value === "")) {
      errors.push({
        field,
        message: `${field} is required`,
      });
      continue;
    }

    if (value === null || value === undefined || value === "") {
      continue;
    }

    // Check type
    if (rule.type) {
      if (
        rule.type === "email" &&
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
      ) {
        errors.push({
          field,
          message: `${field} must be a valid email`,
        });
      } else if (
        rule.type === "url" &&
        !isValidUrl(value)
      ) {
        errors.push({
          field,
          message: `${field} must be a valid URL`,
        });
      } else if (
        rule.type !== "string" &&
        typeof value !== rule.type
      ) {
        errors.push({
          field,
          message: `${field} must be of type ${rule.type}`,
        });
      }
    }

    // Check string rules
    if (typeof value === "string") {
      if (rule.minLength && value.length < rule.minLength) {
        errors.push({
          field,
          message: `${field} must be at least ${rule.minLength} characters`,
        });
      }

      if (rule.maxLength && value.length > rule.maxLength) {
        errors.push({
          field,
          message: `${field} must be at most ${rule.maxLength} characters`,
        });
      }

      if (rule.pattern && !rule.pattern.test(value)) {
        errors.push({
          field,
          message: `${field} format is invalid`,
        });
      }
    }

    // Check number rules
    if (typeof value === "number") {
      if (rule.min !== undefined && value < rule.min) {
        errors.push({
          field,
          message: `${field} must be at least ${rule.min}`,
        });
      }

      if (rule.max !== undefined && value > rule.max) {
        errors.push({
          field,
          message: `${field} must be at most ${rule.max}`,
        });
      }
    }

    // Check custom validation
    if (rule.custom) {
      const result = rule.custom(value);
      if (result !== true) {
        errors.push({
          field,
          message: typeof result === "string" ? result : `${field} is invalid`,
        });
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate URL
 */
function isValidUrl(string: string): boolean {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

export default {
  validateRequest,
};
