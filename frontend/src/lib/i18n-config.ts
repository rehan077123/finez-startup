// i18n config for locale detection
export const defaultLocale = 'en';
export const locales = ['en', 'hi', 'ta', 'bn'] as const;
export type Locale = (typeof locales)[number];

export function isValidLocale(locale: string): locale is Locale {
  return locales.includes(locale as Locale);
}
