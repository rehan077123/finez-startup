import { getRequestConfig } from "next-intl/server";
import { locales, defaultLocale } from "@/lib/i18n-config";

export default getRequestConfig(async ({ locale }) => {
  // Ensure we have a valid locale, fallback to default
  const activeLocale = locale || defaultLocale;
  
  return {
    locale: activeLocale,
    messages: (await import(`../../messages/${activeLocale}.json`)).default,
  };
});
