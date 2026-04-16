# Testing Guide

## Unit Tests

### Setup Jest
```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

### Example Test
```typescript
// src/__tests__/utils.test.ts
import { formatCurrency, truncate } from '@/lib/utils';

describe('utils', () => {
  describe('formatCurrency', () => {
    it('formats currency correctly', () => {
      expect(formatCurrency(1000)).toBe('₹1,000.00');
    });
  });

  describe('truncate', () => {
    it('truncates long text', () => {
      expect(truncate('Hello World', 5)).toBe('Hello...');
    });
  });
});
```

## Integration Tests

### API Route Testing
```typescript
// src/__tests__/api.test.ts
import { createClient } from '@supabase/supabase-js';

describe('API Routes', () => {
  it('fetches products correctly', async () => {
    const response = await fetch('/api/products?limit=10');
    const data = await response.json();
    
    expect(response.status).toBe(200);
    expect(data.products).toBeDefined();
    expect(Array.isArray(data.products)).toBe(true);
  });

  it('tracks affiliate clicks', async () => {
    const response = await fetch('/api/go/test-product-id');
    expect(response.status).toBe(307); // Redirect
  });
});
```

## E2E Tests with Playwright

### Setup
```bash
npm install --save-dev @playwright/test
npx playwright install
```

### Example Test
```typescript
// e2e/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('loads and displays products', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Check title
    await expect(page).toHaveTitle(/FineZ/);
    
    // Check heading
    const heading = page.getByRole('heading', { name: /Smart Product Discovery/ });
    await expect(heading).toBeVisible();
  });

  test('affiliate link redirects correctly', async ({ page }) => {
    await page.goto('http://localhost:3000/products');
    
    const buyButton = page.getByRole('link', { name: /Buy Now/ }).first();
    
    const [popup] = await Promise.all([
      page.waitForEvent('popup'),
      buyButton.click()
    ]);
    
    expect(popup.url()).toContain('amazon');
  });
});
```

## Run Tests

```bash
# Unit tests
npm test

# E2E tests
npx playwright test

# E2E tests with UI
npx playwright test --ui

# E2E tests specific file
npx playwright test e2e/homepage.spec.ts
```

## Load Testing

### Using Artillery
```bash
npm install --save-dev artillery

# Run load test
artillery quick --count 100 --num 10 http://localhost:3000/api/products
```

### Load Test Configuration
```yaml
# load-test.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: 'Browse Products'
    flow:
      - get:
          url: '/api/products'
      - think: 5
      - get:
          url: '/api/products/{{ productId }}'
```

## Performance Testing

### Lighthouse CI
```bash
npm install --save-dev @lhci/cli@0.9.x @lhci/config-reader@0.9.x
```

### lighthouse.config.js
```js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      staticDistDir: './out',
    },
    assert: {
      preset: 'lighthouse:recommended',
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

## Manual Testing Checklist

### Functionality
- [ ] Products load
- [ ] Search works
- [ ] Filters work
- [ ] Affiliate clicks redirect
- [ ] Price alerts save
- [ ] Saved searches display

### Mobile (Android)
- [ ] App installs from home screen
- [ ] App loads offline
- [ ] Touch interactions work
- [ ] Layout responsive
- [ ] Icons display correctly

### Browser
- [ ] Chrome works
- [ ] Firefox works
- [ ] Safari works
- [ ] Edge works

### Performance
- [ ] Page loads < 2.5s
- [ ] Interactive < 100ms
- [ ] CLS < 0.1
- [ ] Images optimized
- [ ] No console errors

### Security
- [ ] HTTPS enforced
- [ ] No sensitive data in logs
- [ ] CORS headers correct
- [ ] CSP headers set

## CI/CD Integration

### GitHub Actions
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run type-check
      - run: npm run lint
      - run: npm test
      - run: npm run build
  
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run build
      - run: npm start &
      - run: npx playwright test --headed
```

## Test Coverage

### Track Coverage
```bash
npm test -- --coverage
```

### Coverage Goals
- Statements: > 70%
- Branches: > 60%
- Functions: > 70%
- Lines: > 70%

---

**Target**: 80%+ coverage before production
