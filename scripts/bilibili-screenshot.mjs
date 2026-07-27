import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

await page.goto('https://www.bilibili.com', { waitUntil: 'networkidle', timeout: 30000 });

// Wait for the main content to be visible
await page.waitForSelector('.bili-header__channel, .home-content, #internationalHeader, .bili-feed', {
  timeout: 15000,
}).catch(() => {});

// Give dynamic content a moment to load
await page.waitForTimeout(2000);

await page.screenshot({ path: 'C:\\Users\\11428\\Desktop\\mftui\\bilibili-homepage.png', fullPage: false });

const title = await page.title();
const url = page.url();

console.log(`Page title: ${title}`);
console.log(`URL: ${url}`);
console.log('Screenshot saved to bilibili-homepage.png');

await browser.close();
