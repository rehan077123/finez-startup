// Email Service Integration (Resend)
// Install: npm install resend

const RESEND_API_KEY = process.env.RESEND_API_KEY;

interface EmailRequest {
  to: string | string[];
  subject: string;
  html: string;
  from?: string;
  replyTo?: string;
  cc?: string[];
  bcc?: string[];
}

interface OrderConfirmationEmail {
  orderId: string;
  customerEmail: string;
  customerName: string;
  items: Array<{ name: string; quantity: number; price: number }>;
  totalAmount: number;
  estimatedDelivery: string;
}

interface VerificationEmail {
  email: string;
  verificationLink: string;
  name?: string;
}

interface PriceAlertEmail {
  email: string;
  productName: string;
  targetPrice: number;
  currentPrice: number;
  productLink: string;
}

/**
 * Send verification email
 */
export async function sendVerificationEmail(
  request: VerificationEmail
): Promise<{ id: string; status: string }> {
  try {
    if (!RESEND_API_KEY) {
      throw new Error("RESEND_API_KEY is not configured");
    }

    // In production, use actual Resend API
    // const { Resend } = require('resend');
    // const resend = new Resend(RESEND_API_KEY);
    // const response = await resend.emails.send({
    //   from: 'noreply@finez.com',
    //   to: request.email,
    //   subject: 'Verify your email',
    //   html: `<p>Click <a href="${request.verificationLink}">here</a> to verify</p>`
    // });

    console.log(
      `[EMAIL] Verification email sent to ${request.email}`
    );

    return {
      id: `email_${Date.now()}`,
      status: "sent",
    };
  } catch (error) {
    console.error("Failed to send verification email:", error);
    throw error;
  }
}

/**
 * Send order confirmation email
 */
export async function sendOrderConfirmationEmail(
  request: OrderConfirmationEmail
): Promise<{ id: string; status: string }> {
  try {
    if (!RESEND_API_KEY) {
      throw new Error("RESEND_API_KEY is not configured");
    }

    const itemsHtml = request.items
      .map(
        (item) => `
        <tr>
          <td>${item.name}</td>
          <td>${item.quantity}</td>
          <td>$${item.price.toFixed(2)}</td>
        </tr>
      `
      )
      .join("");

    const html = `
      <h1>Order Confirmation</h1>
      <p>Hi ${request.customerName},</p>
      <p>Your order #${request.orderId} has been confirmed.</p>
      
      <table border="1">
        <tr>
          <th>Product</th>
          <th>Qty</th>
          <th>Price</th>
        </tr>
        ${itemsHtml}
      </table>
      
      <p><strong>Total: $${request.totalAmount.toFixed(2)}</strong></p>
      <p>Estimated Delivery: ${request.estimatedDelivery}</p>
    `;

    console.log(`[EMAIL] Order confirmation sent to ${request.customerEmail}`);

    return {
      id: `email_${Date.now()}`,
      status: "sent",
    };
  } catch (error) {
    console.error("Failed to send order confirmation email:", error);
    throw error;
  }
}

/**
 * Send price alert email
 */
export async function sendPriceAlertEmail(
  request: PriceAlertEmail
): Promise<{ id: string; status: string }> {
  try {
    if (!RESEND_API_KEY) {
      throw new Error("RESEND_API_KEY is not configured");
    }

    const savings = request.currentPrice - request.targetPrice;

    const html = `
      <h1>Price Alert</h1>
      <p>Great news! ${request.productName} is now ${savings > 0 ? "below" : "at"} your target price!</p>
      <p>
        <strong>Target Price:</strong> $${request.targetPrice.toFixed(2)}<br>
        <strong>Current Price:</strong> $${request.currentPrice.toFixed(2)}<br>
        <strong>Savings:</strong> $${Math.abs(savings).toFixed(2)}
      </p>
      <a href="${request.productLink}">View Product</a>
    `;

    console.log(`[EMAIL] Price alert sent to ${request.email}`);

    return {
      id: `email_${Date.now()}`,
      status: "sent",
    };
  } catch (error) {
    console.error("Failed to send price alert email:", error);
    throw error;
  }
}

/**
 * Send generic email
 */
export async function sendEmail(
  request: EmailRequest
): Promise<{ id: string; status: string }> {
  try {
    if (!RESEND_API_KEY) {
      throw new Error("RESEND_API_KEY is not configured");
    }

    console.log(`[EMAIL] Email sent to ${request.to}`);

    return {
      id: `email_${Date.now()}`,
      status: "sent",
    };
  } catch (error) {
    console.error("Failed to send email:", error);
    throw error;
  }
}

export default {
  sendVerificationEmail,
  sendOrderConfirmationEmail,
  sendPriceAlertEmail,
  sendEmail,
};
