<?php $title = 'Settings'; ?>
<h1 class="reveal">Settings</h1>
<form method="post" class="card form reveal">
  <?= csrf_field() ?>
  <h2>Brand</h2>
  <label>Brand name<input name="brand_name" maxlength="80" value="<?= e(setting('brand_name')) ?>"></label>
  <label>Splash line under the name (app opening screen)<input name="splash_subtitle" maxlength="40" value="<?= e(setting('splash_subtitle')) ?>"></label>
  <label>Promise shown to clients<input name="promise_text" maxlength="200" value="<?= e(setting('promise_text')) ?>"></label>
  <label>Tagline<input name="brand_tagline" maxlength="160" value="<?= e(setting('brand_tagline')) ?>"></label>
  <label>Your email for new-order alerts<input name="owner_email" type="email" maxlength="190" value="<?= e(setting('owner_email')) ?>"></label>
  <label>Send emails from <small>(an address of your domain made in cPanel → Email Accounts, e.g. no-reply@firecraft.fun; empty = no emails)</small><input name="mail_from" type="email" maxlength="190" value="<?= e(setting('mail_from')) ?>"></label>
  <label>Privacy text<textarea name="privacy_text" rows="3" maxlength="5000"><?= e(setting('privacy_text')) ?></textarea></label>
  <label>Support contact shown to clients<input name="support_contact" maxlength="200" value="<?= e(setting('support_contact')) ?>"></label>
  <h2>Rates (per second of finished video)</h2>
  <div class="grid2">
    <label>PKR per second<input name="rate_pkr" type="number" step="0.0001" min="0" value="<?= e(setting('rate_pkr')) ?>"></label>
    <label>USD per second<input name="rate_usd" type="number" step="0.0001" min="0" value="<?= e(setting('rate_usd')) ?>"></label>
  </div>
  <p class="muted">Example: 60 s at <?= e(setting('rate_pkr')) ?> PKR = <?= e(fmt_money(60 * (float) setting('rate_pkr'), 'PKR')) ?>. Per-client rates: Clients page.</p>
  <h2>Uploads</h2>
  <div class="grid2">
    <label>Max size per file (MB)<input name="max_file_mb" type="number" min="10" max="20480" value="<?= e(setting('max_file_mb')) ?>"></label>
    <label>Max files per order<input name="max_files_per_order" type="number" min="1" max="500" value="<?= e(setting('max_files_per_order')) ?>"></label>
    <label>Storage per client (GB)<input name="quota_gb" type="number" min="1" max="10000" value="<?= e(setting('quota_gb')) ?>"></label>
    <label>New accounts<select name="signup_approval"><option value="1">Wait for my approval (paid clients only)</option><option value="0" <?= setting('signup_approval') === '0' ? 'selected' : '' ?>>Open for everyone</option></select></label>
  </div>
  <p class="muted">Upload part size on this server: <?= e(fmt_bytes($chunk)) ?>. PHP: <?php foreach ($ini as $k => $v) echo e("$k=$v") . ' '; ?></p>
  <h2>Android app</h2>
  <div class="grid2">
    <label>Published app version (versionCode of the uploaded APK)<input name="app_version" type="number" min="0" value="<?= e(setting('app_version')) ?>"></label>
    <label>What's new (shown in the update message)<input name="app_notes" maxlength="300" value="<?= e(setting('app_notes')) ?>"></label>
  </div>
  <div class="grid2">
    <label>Live update version (x.y.z of the uploaded bundle.zip)<input name="bundle_version" pattern="\d+\.\d+\.\d+" value="<?= e(setting('bundle_version')) ?>"></label>
    <label>Bundle needs app version at least<input name="bundle_min_native" type="number" min="0" value="<?= e(setting('bundle_min_native')) ?>"></label>
  </div>
  <p class="muted">Two kinds of update: (1) <strong>Live update</strong> = new app screens/features: upload bundle.zip (made by
    portal/mobile/build_bundle.sh), set its version, save: every app downloads it by itself, no reinstall.
    (2) <strong>New APK</strong> = only for native changes (icon, name, plugins): upload it, raise the app version: phones show "Update".</p>
  <button class="btn primary">Save settings</button>
</form>
<section class="card reveal">
  <h2>App file (APK)</h2>
  <p class="muted"><?= $apkSize ? 'Current APK: ' . e(fmt_bytes((int) $apkSize)) . ' · public link: ' . e(base_url('app/download')) : 'No APK uploaded yet.' ?></p>
  <div class="drop" data-uploader data-order="0" data-kind="apk" data-reload="1" tabindex="0">
    <input type="file" id="pick" accept=".apk"><label for="pick" class="btn">Upload APK</label>
  </div>
  <ul class="file-list" data-file-list></ul>
  <h2>Live update bundle</h2>
  <p class="muted"><?= $bundleSize ? 'Current bundle: ' . e(fmt_bytes((int) $bundleSize)) . ' · version ' . e(setting('bundle_version')) : 'No bundle uploaded yet.' ?></p>
  <div class="drop" data-uploader data-order="0" data-kind="bundle" data-reload="1" tabindex="0">
    <input type="file" id="pickb" accept=".zip"><label for="pickb" class="btn">Upload bundle.zip</label>
  </div>
  <ul class="file-list" data-file-list></ul>
</section>
<section class="card reveal">
  <h2>Claude bridge token</h2>
  <?php if ($newToken): ?>
    <p class="notice ok">New token (shown only once, copy it now and save it as the PORTAL_BRIDGE_TOKEN secret of the Claude environment):</p>
    <p><code class="token"><?= e($newToken) ?></code></p>
  <?php else: ?>
    <p class="muted"><?= setting('bridge_token_hash') ? 'A token is set. Making a new one stops the old one.' : 'No token yet: the bridge cannot connect.' ?></p>
  <?php endif; ?>
  <form method="post" class="form"><?= csrf_field() ?><input type="hidden" name="action" value="token">
    <button class="btn" data-confirm="Make a new token? The old one stops working.">Make new token</button></form>
  <h3>Recent bridge events</h3>
  <ul class="file-list"><?php foreach ($events as $ev): ?><li>#<?= (int) $ev['order_id'] ?> <?= e($ev['title']) ?> · <?= e($ev['type']) ?> · <?= e(fmt_date($ev['created_at'])) ?> · <?= $ev['done_at'] ? 'done' : ($ev['taken_at'] ? 'taken' : 'waiting') ?></li><?php endforeach; ?></ul>
</section>
