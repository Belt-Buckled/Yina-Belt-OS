const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1024, height: 1536 }, deviceScaleFactor: 2 });
  for (const n of ['01-warm-archive','02-marquee','03-quiet-table']) {
    await p.goto('file://' + process.cwd() + '/' + n + '.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(2500);
    const ok = await p.evaluate(() => ({
      caveat: document.fonts.check('16px Caveat'),
      archivo: document.fonts.check('800 16px Archivo'),
      bodoni: document.fonts.check('16px "Bodoni Moda"'),
      corm: document.fonts.check('300 16px "Cormorant Garamond"'),
      jost: document.fonts.check('16px Jost')
    }));
    console.log(n, JSON.stringify(ok));
    await p.screenshot({ path: n + '.png', fullPage: true });
  }
  await b.close();
})();
