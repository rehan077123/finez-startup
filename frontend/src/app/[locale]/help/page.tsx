"use client";

import { useState } from "react";
import { Card, Button, Input, Spinner } from "@/components/ui";
import { MessageSquare, Send, Phone } from "lucide-react";

interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
}

export default function HelpPage() {
  const [expanded, setExpanded] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  const faqs: FAQItem[] = [
    {
      id: "1",
      question: "How do I track my order?",
      answer: "You can track your order using the order tracking page. Click on your account, go to orders, and select the order you want to track.",
      category: "Orders",
    },
    {
      id: "2",
      question: "What is your return policy?",
      answer: "We offer 30 days returns on most items. Items must be unused and in original packaging.",
      category: "Returns",
    },
    {
      id: "3",
      question: "How do I set up price alerts?",
      answer: "Go to any product page and click 'Set Price Alert'. Choose your target price and we'll notify you when that price is reached.",
      category: "Features",
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Help & Support
      </h1>
      <p className="text-gray-600 dark:text-gray-400 mb-12">
        Find answers to common questions
      </p>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <Card className="p-6 text-center hover:shadow-lg transition-shadow cursor-pointer">
          <MessageSquare size={32} className="mx-auto text-blue-600 mb-3" />
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Chat with Us
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Available 9 AM - 9 PM EST
          </p>
          <Button className="mt-4 w-full">Start Chat</Button>
        </Card>

        <Card className="p-6 text-center hover:shadow-lg transition-shadow cursor-pointer">
          <Phone size={32} className="mx-auto text-green-600 mb-3" />
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Call Us
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            1-800-FINEZ-1
          </p>
          <Button className="mt-4 w-full">Schedule Call</Button>
        </Card>

        <Card className="p-6 text-center hover:shadow-lg transition-shadow cursor-pointer">
          <MessageSquare size={32} className="mx-auto text-purple-600 mb-3" />
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Email Us
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            support@finez.com
          </p>
          <Button className="mt-4 w-full">Send Email</Button>
        </Card>
      </div>

      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Frequently Asked Questions
      </h2>

      <div className="space-y-4">
        {faqs.map((faq) => (
          <Card key={faq.id} className="overflow-hidden">
            <button
              onClick={() =>
                setExpanded(expanded === faq.id ? null : faq.id)
              }
              className="w-full p-6 text-left hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors flex justify-between items-center"
            >
              <div>
                <p className="text-xs font-semibold text-blue-600 mb-1">
                  {faq.category}
                </p>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {faq.question}
                </p>
              </div>
              <span
                className={`text-2xl transition-transform ${
                  expanded === faq.id ? "rotate-45" : ""
                }`}
              >
                +
              </span>
            </button>
            {expanded === faq.id && (
              <div className="px-6 pb-6 text-gray-600 dark:text-gray-400 border-t border-gray-200 dark:border-slate-700">
                {faq.answer}
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}
