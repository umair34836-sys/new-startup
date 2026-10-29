<?php $title = 'Settings'; ?>
<h1 class="reveal">Settings</h1>
<form method="post" class="card form reveal">
  <?= csrf_field() ?>
  <h2>Brand</h2>
  <label>Brand name<input name="brand_name" maxlength="80" value="<?= e(setting('brand_name')) ?>"></label>
  <label>Tagline<input name="brand_tagline" maxlength="160" value="<?= e(setting('brand_tagline')) ?>"></label>
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
  <button class="btn primary">Save settings</button>
</form>
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
