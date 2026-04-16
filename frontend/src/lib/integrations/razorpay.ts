// Razorpay Payment Integration
// Install: npm install razorpay

const RAZORPAY_KEY_ID = process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID;
const RAZORPAY_KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;

interface CreateOrderRequest {
  amount: number; // in paise (multiply by 100 for INR)
  currency?: string;
  receipt?: string;
  description?: string;
  customer_notify?: number;
}

interface VerifyPaymentRequest {
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
}

interface CreateSubscriptionRequest {
  planId: string;
  customerId: string;
  quantity?: number;
  totalCount?: number;
  addons?: Array<{ item: { name: string; amount: number } }>;
}

/**
 * Create a Razorpay order
 */
export async function createOrder(
  request: CreateOrderRequest
): Promise<{
  id: string;
  entity: string;
  amount: number;
  amount_paid: number;
  amount_due: number;
  currency: string;
  receipt: string;
  status: string;
  attempts: number;
  notes: Record<string, any>;
  created_at: number;
}> {
  try {
    if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
      throw new Error(
        "Razorpay credentials are not configured"
      );
    }

    // In production, use actual Razorpay API
    // const Razorpay = require('razorpay');
    // const razorpay = new Razorpay({
    //   key_id: RAZORPAY_KEY_ID,
    //   key_secret: RAZORPAY_KEY_SECRET
        // });
    // const order = await razorpay.orders.create(request);

    const mockOrder = {
      id: `order_${Date.now()}`,
      entity: "order",
      amount: request.amount,
      amount_paid: 0,
      amount_due: request.amount,
      currency: request.currency || "INR",
      receipt: request.receipt || `receipt_${Date.now()}`,
      status: "created",
      attempts: 0,
      notes: {},
      created_at: Math.floor(Date.now() / 1000),
    };

    return mockOrder;
  } catch (error) {
    console.error("Failed to create Razorpay order:", error);
    throw error;
  }
}

/**
 * Verify payment signature
 */
export async function verifyPaymentSignature(
  request: VerifyPaymentRequest
): Promise<boolean> {
  try {
    if (!RAZORPAY_KEY_SECRET) {
      throw new Error("Razorpay key secret is not configured");
    }

    // In production, verify using crypto
    // const crypto = require('crypto');
    // const body = `${request.razorpay_order_id}|${request.razorpay_payment_id}`;
    // const expectedSignature = crypto
    //   .createHmac('sha256', RAZORPAY_KEY_SECRET)
    //   .update(body)
    //   .digest('hex');
    // return expectedSignature === request.razorpay_signature;

    // Mock verification
    return request.razorpay_signature?.length > 0;
  } catch (error) {
    console.error("Failed to verify payment signature:", error);
    return false;
  }
}

/**
 * Create a subscription plan
 */
export async function createSubscriptionPlan(planData: {
  period: "monthly" | "yearly";
  interval: number;
  amount: number;
  description: string;
}): Promise<{
  id: string;
  interval: number;
  period: string;
  item: { id: string; amount: number };
  notes: Record<string, any>;
  created_at: number;
}> {
  try {
    if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
      throw new Error("Razorpay credentials are not configured");
    }

    // In production, use actual Razorpay API
    const mockPlan = {
      id: `plan_${Date.now()}`,
      interval: planData.interval,
      period: planData.period,
      item: {
        id: `item_${Date.now()}`,
        amount: planData.amount,
      },
      notes: {},
      created_at: Math.floor(Date.now() / 1000),
    };

    return mockPlan;
  } catch (error) {
    console.error("Failed to create subscription plan:", error);
    throw error;
  }
}

/**
 * Create a subscription
 */
export async function createSubscription(
  request: CreateSubscriptionRequest
): Promise<{
  id: string;
  entity: string;
  plan_id: string;
  customer_id: string;
  status: string;
  current_start?: number;
  current_end?: number;
  ended_at?: number;
  quantity: number;
  notes: Record<string, any>;
  created_at: number;
}> {
  try {
    if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
      throw new Error("Razorpay credentials are not configured");
    }

    // In production, use actual Razorpay API
    const mockSubscription = {
      id: `sub_${Date.now()}`,
      entity: "subscription",
      plan_id: request.planId,
      customer_id: request.customerId,
      status: "active",
      current_start: Math.floor(Date.now() / 1000),
      current_end: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60,
      quantity: request.quantity || 1,
      notes: {},
      created_at: Math.floor(Date.now() / 1000),
    };

    return mockSubscription;
  } catch (error) {
    console.error("Failed to create subscription:", error);
    throw error;
  }
}

/**
 * Process a refund
 */
export async function processRefund(
  paymentId: string,
  amount?: number
): Promise<{ id: string; amount: number; status: string }> {
  try {
    if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
      throw new Error("Razorpay credentials are not configured");
    }

    // In production, use actual Razorpay API
    const mockRefund = {
      id: `ref_${Date.now()}`,
      amount: amount || 0,
      status: "processed",
    };

    return mockRefund;
  } catch (error) {
    console.error("Failed to process refund:", error);
    throw error;
  }
}

export default {
  createOrder,
  verifyPaymentSignature,
  createSubscriptionPlan,
  createSubscription,
  processRefund,
};
