import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export default async function middleware( request: NextRequest ) {
  const sessionCookie = cookies().get('session');
  if (sessionCookie) {
    return NextResponse.next()
  }
    // Redirect to login page with a message
  return NextResponse.redirect(new URL('/login', request.url))
}

export const config = {
  matcher: '/home/:path*',
}