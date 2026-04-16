import { NextRequest, NextResponse } from "next/server";

interface TranslateRequest {
  text: string;
  targetLanguage: string;
  sourceLanguage?: string;
}

// Supported languages
const SUPPORTED_LANGUAGES: Record<string, string> = {
  en: "English",
  hi: "Hindi",
  ta: "Tamil",
  bn: "Bengali",
  es: "Spanish",
  fr: "French",
};

// Simple mock translations (in production, use Google Translate API or Anthropic)
function getSimpleTranslation(
  text: string,
  targetLanguage: string
): string {
  // This is a mock. In production, integrate with Google Translate API
  const translations: Record<string, Record<string, string>> = {
    hi: {
      "Best deals online": "सर्वश्रेष्ठ ऑनलाइन डील",
      "Find the best prices": "सर्वोत्तम कीमतें खोजें",
    },
    ta: {
      "Best deals online": "சிறந்த ஆன்லைன் டீல்கள்",
      "Find the best prices": "சிறந்த விலைகளைக் கண்டுபிடிக்கவும்",
    },
    bn: {
      "Best deals online": "সেরা অনলাইন ডিল",
      "Find the best prices": "সেরা দাম খুঁজুন",
    },
  };

  return (
    translations[targetLanguage]?.[text] ||
    text +
      ` [${targetLanguage}]` // Fallback with language code
  );
}

export async function POST(request: NextRequest) {
  try {
    const body: TranslateRequest = await request.json();

    if (!body.text || !body.targetLanguage) {
      return NextResponse.json(
        { error: "text and targetLanguage are required" },
        { status: 400 }
      );
    }

    if (!SUPPORTED_LANGUAGES[body.targetLanguage]) {
      return NextResponse.json(
        {
          error: `Unsupported language: ${body.targetLanguage}`,
          supported: Object.keys(SUPPORTED_LANGUAGES),
        },
        { status: 400 }
      );
    }

    const translatedText = getSimpleTranslation(
      body.text,
      body.targetLanguage
    );

    return NextResponse.json({
      success: true,
      original: body.text,
      translated: translatedText,
      sourceLanguage: body.sourceLanguage || "en",
      targetLanguage: body.targetLanguage,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Translation failed", details: String(error) },
      { status: 500 }
    );
  }
}
