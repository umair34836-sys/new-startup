# FireCraft SMP: real whitelist application flow (www.firecraft.fun)

Checked 2026-10-24 with headless Chromium (Playwright, 1920x1080) and by reading the live page source
(`curl https://www.firecraft.fun/`, `/js/app.js`, `/join/`, `/rules/`). Labels below are copied exactly as seen.
Nothing was submitted: no account was created and no application was sent (Create Account and Submit
Application were only hovered + shown with a click animation in the tutorial recording).

## URLs visited (2026-10-24)
- https://www.firecraft.fun/ (homepage; title "FireCraft SMP | Private Lifesteal Minecraft Server with Custom Powers")
- https://www.firecraft.fun/#apply (form section on the homepage), #status (My Profile)
- https://www.firecraft.fun/join/ ("How to Get Whitelisted" guide)
- https://www.firecraft.fun/rules/ (rules page; source of the rules-check answer)
- https://www.firecraft.fun/js/app.js (form/auth logic, read only)

## Homepage
- Top nav: Home, Apply, My Status, Support, Reviews, Features, Rules, FAQ, Leaderboard, Join, Blog, Discord, Login.
- Hero: "PRIVATE LIFESTEAL SMP — APPLY FREE", "FIRE CRAFT SMP", "11 Custom Elemental Powers • 63 Tameable Mobs • 5 Armor Sets",
  buttons "⚡ Apply for Whitelist", "My Status", "🎮 Discord"; status line "Online — 0/20 players" (at capture time);
  "Server Address play.firecraft.fun:20011" with "Copy".

## Step 1: Create a FireCraft account (Login button, top right)
- Login modal: eyebrow "FIRECRAFT ACCOUNT", heading "Login", "Use your Minecraft IGN and FireCraft password.",
  fields "Minecraft IGN" (hint "Enter the username you registered with"), "Password"; button "Login";
  links "Forgot password?" and "New here? Create FireCraft account".
  Guide box "New here? Here's how to join:" 1 Create Account (Register with your Minecraft IGN) → 2 Apply (Fill the
  whitelist application) → 3 Get Approved (Admin reviews your application) → 🎮 Start Playing! (Join & enjoy FireCraft SMP).
- "New here? Create FireCraft account" opens: progress Create Account / Apply / Get Approved / Play!, eyebrow
  "STEP 1 OF 3", heading "Create Account", "Your IGN is your FireCraft username. Use a strong password."
  Fields: "Minecraft IGN *" (hint "3–16 characters — letters, numbers and underscores only"), "Email Address *"
  (hint "Used for account recovery — never shown publicly"), "Password *" (placeholder "At least 6 characters", hint
  "Choose a strong password you haven't used elsewhere"), "Confirm Password *"; button "Create Account".
  Box "After creating your account:" 2 Go to Apply in the menu and fill the whitelist form; 3 Wait for admin approval
  (usually within 24 hours); 🎮 Join the server with IP shown on website!; link "Already have an account? Login".
- app.js checks: IGN must match `^[A-Za-z0-9_]{3,16}$`, email required, password >= 6 chars, passwords must match;
  success message "Account created. Welcome to FireCraft!".

## Step 2: Whitelist Application (#apply)
- Eyebrow "JOIN FIRECRAFT", heading "Whitelist Application", "Tell the staff who you are and why you want to join."
- Fields (in order):
  1. "Minecraft IGN" (read-only; "Auto-filled from your account — cannot be changed here")
  2. "Java or Bedrock? *" select: Java / Bedrock ("Which Minecraft you will join with")
  3. "Discord username *" (placeholder "e.g. steve123", "So staff can reach you after review")
  4. "Age *" (number 13–99, "You must be at least 13 years old to apply")
  5. "Which days, and at what time, do you usually play? *" ("Include your timezone (PKT / IST / other)")
  6. "How many hours a week can you play in Season 2? *": Less than 3 hours / 3–7 hours / 7–14 hours / 14+ hours
  7. "Did you play Season 1? *": No — I'm new to FireCraft / Yes — I played until the end / Yes — but I stopped playing
  8. "If you stopped playing in Season 1, why?" ("Required only if you stopped playing")
  9. "Rules check: what happens if you break someone else's build at spawn? *" ("The answer is on the rules page")
  10. "Why do you want to join FireCraft, and how did you find us? *" (textarea, "0 / 1000 characters")
  11. "Referred by (optional)" ("Leave empty if nobody invited you")
  12. "Do you agree to follow the FireCraft rules? *": Yes, I agree to all FireCraft rules / No
  Button "Submit Application".
- Logged out, the form can be filled but Submit opens the Login modal (app.js: `if(!u){openAuth();return;}`); logged in it
  writes the application with status "pending" and shows "Application submitted. Staff will review it." (from app.js; not
  seen live because nothing was submitted).
- Rules-check answer on /rules/ (R07 "Spawn Is a Safe Zone"): "Breaking someone else's build at spawn = 2-day ban."
  The tutorial does not reveal it; it only says the answer is on the rules page.

## Step 3: My Status (#status)
- Eyebrow "YOUR ACCOUNT", heading "My Profile"; logged out it shows "Login to view your profile and application status."
- Logged in (app.js): "No application yet" or the latest application's status (e.g. PENDING), IGN, Submitted time, staff note.
- /join/ step 03 "Wait for Approval": "Staff review applications within 24–48 hours. Log in and check My Status on the
  homepage. If approved, you'll see your whitelist status and the server IP."
- Mismatch on the site: the signup box says "usually within 24 hours", /join/ says "24–48 hours". The video uses 24–48.

## Recording notes
- The page loads Google AdSense + third-party ad scripts (googlesyndication, doubleclick, fundingchoicesmessages,
  adtrafficquality, n6wxm.com vignette, rtmark.net, ldrws.com); they were blocked in the recording so no ad overlays cover the UI.
- At window heights below ~900 CSS px the login modal's top (and its × button) sits under the fixed header, so a click
  on × hits the header (it opened Leaderboard once). The recording reloads the homepage instead of closing the modal.
- Tool: library/tools/screen_recorder.js (zoom 1.25 = page laid out ~1536x864, rendered sharp at 1920x1080).
