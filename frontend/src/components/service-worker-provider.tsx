'use client';

import { useEffect } from 'react';
import { toast } from 'sonner';

export function ServiceWorkerProvider() {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      const handleControllerChange = () => {
        toast.success('App updated! Refresh to see latest changes.', {
          duration: 5000,
          action: {
            label: 'Refresh',
            onClick: () => window.location.reload(),
          },
        });
      };

      navigator.serviceWorker
        .register('/sw.js')
        .then((registration) => {
          console.log('Service Worker registered:', registration);
          setInterval(() => {
            registration.update().catch((err) => {
              console.log('Service Worker update check failed:', err);
            });
          }, 60000);
        })
        .catch((error) => {
          console.warn('Service Worker registration failed:', error);
        });

      navigator.serviceWorker.addEventListener('controllerchange', handleControllerChange);

      return () => {
        navigator.serviceWorker.removeEventListener('controllerchange', handleControllerChange);
      };
    }
    return undefined;
  }, []);

  return null;
}
