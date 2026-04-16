// Service Worker to suppress resource load errors for cross-origin images

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // List of known problematic domains
  const blockedDomains = [
    'zerodha.com',
    'youtube.com',
    'developer.android.com',
    'www.youtube.com',
  ];
  
  // Check if this is a blocked domain
  const isBlocked = blockedDomains.some(domain => url.hostname.includes(domain));
  
  if (isBlocked && (event.request.destination === 'image' || event.request.url.includes('.svg') || event.request.url.includes('.png'))) {
    // Return a 1x1 transparent PNG instead of fetching
    event.respondWith(
      new Response(
        new Blob([
          '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        ], { type: 'image/png' }),
        { 
          status: 200, 
          statusText: 'OK',
          headers: { 'Content-Type': 'image/png' }
        }
      )
    );
  } else {
    // Pass through
    event.respondWith(fetch(event.request));
  }
});
