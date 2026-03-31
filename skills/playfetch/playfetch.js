#!/usr/bin/env node
/** playfetch — загрузка страниц через Playwright */
const { chromium } = require('playwright');

async function main() {
    if (process.argv.length < 3) {
        console.error('Usage: node playfetch.js <url>');
        process.exit(1);
    }

    const url = process.argv[2];

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url, { timeout: 30000 });
    const content = await page.content();
    console.log(content);
    await browser.close();
}

main().catch(e => {
    console.error(e);
    process.exit(1);
});
