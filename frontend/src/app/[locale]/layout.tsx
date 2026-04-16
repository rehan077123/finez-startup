import { notFound } from 'next/navigation';
import { defaultLocale, isValidLocale } from '@/lib/i18n-config';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export const dynamicParams = false;

export function generateStaticParams() {
  return [
    { locale: 'en' },
    { locale: 'hi' },
    { locale: 'ta' },
    { locale: 'bn' },
  ];
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  // Validate locale
  if (!isValidLocale(params.locale)) {
    notFound();
  }

  // Providing all messages to the client
  // side is the easiest way to get started
  const messages = await getMessages();

  return (
    <NextIntlClientProvider messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
