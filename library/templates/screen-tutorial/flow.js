// Records the real FireCraft whitelist flow. Never submits anything: Create Account and Submit Application are fakeClicks.
const { Recorder } = require('/home/user/new-startup/library/tools/screen_recorder.js');
const ADS = [/googlesyndication/, /doubleclick/, /fundingchoicesmessages/, /adtrafficquality/, /n6wxm\.com/, /rtmark\.net/, /ldrws\.com/, /googleadservices/];
(async () => {
  const out = process.argv[2];
  const rec = await Recorder.launch({ out, zoom: 1.25, block: ADS });
  const p = rec.page;
  await rec.goto('https://www.firecraft.fun/', { wait: 3000 });
  await rec.mark('s1_login');
  await rec.click('#authBtn', { label: 'Login', after: 2600 });
  await rec.mark('s2_signup');
  await rec.click('#showSignup', { label: 'New here? Create FireCraft account', after: 1800 });
  await rec.type('#signupIgn', 'DemoPlayer');
  await rec.type('#signupEmail', 'demo@example.com');
  await rec.type('#signupPassword', 'demo1234');
  await rec.type('#signupPassword2', 'demo1234');
  await rec.fakeClick('#signupForm button.btn', { label: 'Create Account (not clicked)', after: 1500 });
  await rec.mark('s3_apply');
  // the modal's close button sits under the site's fixed header at this size: cut to a fresh load instead
  await rec.goto('https://www.firecraft.fun/', { wait: 1500 });
  await rec.click('#nav a[href="#apply"], header a[href="#apply"]', { label: 'Apply', after: 1600 });
  await rec.select('#appEdition', 'Java');
  await rec.type('#appDiscord', 'demo_player');
  await rec.type('#appAge', '18');
  await rec.type('#appPlayTimes', 'Weekdays 8-11 PM PKT');
  await rec.select('#appHours', '3–7 hours');
  await rec.select('#appSeason1', "No — I'm new to FireCraft");
  await rec.mark('s4_rules');
  await rec.type('#appRulesAnswer', 'Demo answer (read the rules page)');
  await rec.type('#appWhy', 'Demo text: I want to play with friends.', { delay: 40 });
  await rec.select('#appRules', 'yes');
  await rec.fakeClick('#applicationForm button[type=submit]', { label: 'Submit Application (not clicked)', after: 1500 });
  await rec.mark('s5_status');
  await rec.click('#nav a[href="#status"], header a[href="#status"]', { label: 'My Status', after: 3500 });
  const r = await rec.finish();
  console.log(JSON.stringify(r));
})().catch(e => { console.error(e); process.exit(1); });
