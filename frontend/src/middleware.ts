import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const locales = ['en', 'hi', 'ta', 'bn'];
const defaultLocale = 'en';

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  // Skip middleware for static files, API, and Next internals
  if (
    pathname.startsWith('/api') ||
    pathname.startsWith('/_next') ||
    pathname.startsWith('/public') ||
    pathname === '/favicon.ico' ||
    /\.(png|jpg|jpeg|gif|svg|webp|css|js)$/i.test(pathname)
  ) {
    return NextResponse.next();
  }

  // Check if path already has locale prefix
  const pathnameHasLocale = locales.some(locale => {
    return pathname === `/${locale}` || pathname.startsWith(`/${locale}/`);
  });

  // If path already has locale, continue
  if (pathnameHasLocale) {
    return NextResponse.next();
  }

  // Redirect root to /en
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/en', request.url));
  }

  // Redirect all other paths to /en/path
  return NextResponse.redirect(new URL(`/en${pathname}`, request.url));
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|public|.*\\.(?:png|jpg|jpeg|gif|svg|webp|css|js)).*)',
  ],
};
