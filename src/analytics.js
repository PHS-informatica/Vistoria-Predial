// Initialize Vercel Web Analytics
import { inject } from '@vercel/analytics';

// Inject analytics tracking with production mode
inject({
  mode: 'production',
});
