// Record https://bhupendra.pages.dev/ at 1920x1080 for the portfolio walkthrough (Heaven Developer job, 2026-10-28).
// Every nav click is shown with the recorder's cursor + ripple (owner rule for screen videos); links that leave the site
// (Work with me, guns.lol, YouTube, Discord) are fakeClick only. Marks = one per VO line for build_bhupendra.py.
//   NODE_PATH="$(npm root -g)" node record_bhupendra.js OUT_DIR
const { Recorder } = require('/home/user/new-startup/library/tools/screen_recorder.js');
const out = process.argv[2];
(async () => {
  const rec = await Recorder.launch({ out, width: 1920, height: 1080, zoom: 1.25 });
  const smooth = async (dy, ms) => {            // slow, even scroll by dy px over ms
    const steps = Math.round(ms / 40);
    for (let i = 0; i < steps; i++) { await rec.page.mouse.wheel(0, dy / steps); await rec.wait(40); }
  };
  await rec.goto('https://bhupendra.pages.dev/', { wait: 2500 });
  await rec.mark('hero'); await rec.wait(2500);
  await rec.fakeClick('a[href*="discord.com/users"]', { label: 'Work with me', after: 1200 });
  await rec.mark('about'); await rec.click('nav a[href="#about"]', { after: 1600 });
  await smooth(700, 4000);
  await rec.mark('whatido'); await smooth(500, 3500);
  await rec.mark('skills'); await rec.click('nav a[href="#skills"]', { after: 1600 });
  await smooth(450, 3000);
  await rec.mark('projects'); await rec.click('nav a[href="#projects"]', { after: 1800 });
  await smooth(200, 1500);
  await rec.fakeClick('a[href*="discord.gg"]', { label: 'Join Heaven Developer', after: 900 });
  await rec.mark('experience'); await rec.click('nav a[href="#experience"]', { after: 1600 });
  await smooth(500, 3000);
  await rec.mark('howiwork'); await smooth(450, 3000);
  await rec.mark('contact'); await rec.click('nav a[href="#contact"]', { after: 1600 });
  await rec.fakeClick('a[href*="guns.lol"] >> nth=-1', { label: 'guns.lol', after: 900 });
  await rec.fakeClick('a[href*="youtube.com"]', { label: 'YouTube', after: 900 });
  await rec.mark('faq'); await smooth(600, 3500);
  await rec.mark('footer'); await smooth(400, 2000); await rec.wait(1500);
  await rec.finish();
})().catch(e => { console.error(e); process.exit(1); });
