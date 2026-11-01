---
name: browser-testing
version: 1.0.0
description: Automated web UI verification, Playwright/Puppeteer automation, and dev endpoint testing using context.local.md.
triggers: ["browser", "playwright", "puppeteer", "ui-test", "login-test", "headless", "screenshot"]
---

# Skill: Browser Testing & Local UI Verification

## Overview
Automated procedures for conducting headful or headless browser testing, verifying web UI flows, performing login checks using mock fixtures from `context.local.md`, and preventing credential amnesia.

## When to Activate
- When verifying frontend web pages, UI components, forms, or authentication flows.
- When running Playwright, Puppeteer, or Chrome DevTools automated actions.
- When capturing screenshots or checking console errors on local dev servers.

## Workflows & Procedures

### 1. Pre-Flight Credential Resolution (The Mock Vault Rule)
* **Rule:** Before launching any browser test or asking the user for test logins, **ALWAYS read `context.local.md`**.
* Locate the seed user or admin account under Section 2:
  ```markdown
  | Role | Username / Email | Mock Password |
  | Admin | admin@test.local | adminpass123 |
  ```
* NEVER hardcode real passwords or live user accounts into test scripts.

### 2. Playwright Quick Verification Script Pattern
```javascript
import { test, expect } from '@playwright/test';

test('Verify dev portal and mock login', async ({ page }) => {
  // Navigate to local frontend URL defined in context.local.md
  await page.goto('http://localhost:3000');

  // Verify page title
  await expect(page).toHaveTitle(/Dev/);

  // Fill credentials from context.local.md
  await page.fill('input[name="email"]', 'admin@test.local');
  await page.fill('input[name="password"]', 'adminpass123');
  await page.click('button[type="submit"]');

  // Assert dashboard entry
  await expect(page.locator('text=Dashboard')).toBeVisible();
});
```

### 3. Capturing Visual Evidence & Debugging
* Always save screenshots of failed assertions in a local temporary directory:
  ```javascript
  await page.screenshot({ path: 'scratch/error-state.png', fullPage: true });
  ```
* Review browser console errors:
  ```javascript
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));
  ```
