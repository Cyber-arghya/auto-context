---
name: browser-testing
version: 1.0.0
description: Automated web UI verification, Playwright/Puppeteer automation, and dev endpoint testing with environment isolation.
triggers: ["browser", "playwright", "puppeteer", "ui-test", "login-test", "headless", "screenshot"]
---

# Skill: Browser Testing & Local UI Verification

## Overview
Automated procedures for conducting headful or headless browser testing, verifying web UI flows, performing assertions using environment-isolated test fixtures, and capturing failure screenshots.

## When to Activate
- When verifying frontend web pages, UI components, forms, or authentication flows.
- When running Playwright, Puppeteer, or Chrome DevTools automated actions.
- When capturing screenshots or checking console errors on local dev servers.

## Workflows & Procedures

### 1. Test Environment & Credential Isolation
* **Rule:** Never hardcode passwords or production accounts in test scripts.
* Load test targets and credentials via `.env.test` or system environment variables:
  ```javascript
  const BASE_URL = process.env.TEST_URL || 'http://localhost:3000';
  const TEST_USER = process.env.TEST_USER_EMAIL;
  const TEST_PASS = process.env.TEST_USER_PASSWORD;
  ```

### 2. Playwright Quick Verification Script Pattern
```javascript
import { test, expect } from '@playwright/test';

test('Verify web portal and authenticated flow', async ({ page }) => {
  const targetUrl = process.env.TEST_URL || 'http://localhost:3000';
  await page.goto(targetUrl);

  // Verify page title
  await expect(page).toHaveTitle(/App|Portal/i);

  // Authenticate if credentials are provided in test environment
  if (process.env.TEST_USER_EMAIL && process.env.TEST_USER_PASSWORD) {
    await page.fill('input[type="email"]', process.env.TEST_USER_EMAIL);
    await page.fill('input[type="password"]', process.env.TEST_USER_PASSWORD);
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Dashboard')).toBeVisible();
  }
});
```

### 3. Capturing Visual Evidence & Debugging
* Always save screenshots of failed assertions in a local temporary directory (`scratch/` or `.tmp/`):
  ```javascript
  await page.screenshot({ path: 'scratch/error-state.png', fullPage: true });
  ```
* Capture browser console errors:
  ```javascript
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));
  ```
