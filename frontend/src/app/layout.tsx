import type { Metadata, Viewport } from 'next';
import { ThemeProvider } from '@/components/theme-provider';
import { Navbar } from '@/components/navbar';
import { Toaster } from 'sonner';
import { ServiceWorkerProvider } from '@/components/service-worker-provider';
import './globals.css';

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
};

export const metadata: Metadata = {
  title: 'FineZ - Smart Product Discovery',
  description:
    'Discover products curated for your lifestyle with AI-powered recommendations and price alerts.',
  keywords: [
    'products',
    'shopping',
    'recommendations',
    'affiliate',
    'discounts',
    'AI',
  ],
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'FineZ',
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
    title: 'FineZ - Smart Product Discovery',
    description:
      'Discover products curated for your lifestyle with AI-powered recommendations and price alerts.',
    siteName: 'FineZ',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'FineZ - Smart Product Discovery',
    description:
      'Discover products curated for your lifestyle with AI-powered recommendations and price alerts.',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="theme-color" content="#000000" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <ServiceWorkerProvider />
          <Navbar />
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
