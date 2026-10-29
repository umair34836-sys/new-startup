<?php
$title = 'New order';
$a = order_answers($order);
$rate = rate_for($user, $order['currency']);
?>
<div class="head-row reveal"><h1>New video order</h1><span class="badge s-draft">Draft #<?= (int) $order['id'] ?></span></div>
<?php foreach ($errors as $er): ?><p class="notice err" role="alert"><?= e($er) ?></p><?php endforeach; ?>

<section class="card reveal">
  <h2>1. Your files <small class="opt">(optional)</small></h2>
  <p class="muted">Raw videos, photos, logo, voice notes, script (PDF/DOCX/TXT), if you have them. No files? No problem: just
    describe the video below. Big files upload in small parts, so keep this page open until each one shows "Uploaded".</p>
  <p class="req-note">Fields marked <span class="req">*</span> are required.</p>
  <div class="drop" data-uploader data-order="<?= (int) $order['id'] ?>" data-kind="input" tabindex="0">
    <input type="file" id="pick" multiple accept="video/*,image/*,audio/*,.pdf,.txt,.srt,.docx,.zip">
    <label for="pick" class="btn">Choose files</label>
    <span>or drop them here</span>
  </div>
  <ul class="file-list" data-file-list>
    <?php foreach ($files as $f): ?>
      <li><span class="fname"><?= e($f['orig_name']) ?></span><span class="muted"><?= e(fmt_bytes((int) $f['size'])) ?></span>
        <button class="link danger" form="del-<?= (int) $f['id'] ?>">Remove</button></li>
    <?php endforeach; ?>
  </ul>
</section>

<form method="post" action="<?= e(base_url('orders/' . $order['id'] . '/save')) ?>" class="form" id="order-form">
  <?= csrf_field() ?>
  <section class="card reveal">
    <h2>2. About the video</h2>
    <label>Video name <span class="req">*</span><input name="title" maxlength="160" required value="<?= e($order['title'] === 'New video' ? '' : $order['title']) ?>" placeholder="e.g. Shop opening reel"></label>
    <label>Length of the finished video (seconds) <span class="req">*</span>
      <input name="length_sec" type="number" min="1" max="36000" required value="<?= (int) $order['length_sec'] ?: '' ?>" data-length></label>
    <p class="estimate" data-estimate data-rate="<?= e((string) $rate) ?>" data-currency="<?= e($order['currency']) ?>">
      Price estimate: <strong data-estimate-value><?= e(fmt_money(estimate((int) $order['length_sec'], $rate), $order['currency'])) ?></strong>
      <small>(<?= e(fmt_money($rate, $order['currency'])) ?> per second)</small></p>
    <div class="grid2">
    <?php foreach (questions() as $key => $qq): $val = $a[$key] ?? ''; ?>
      <label><?= e($qq['label']) ?> <?= $qq['required'] ? '<span class="req">*</span>' : '<small class="opt">(optional)</small>' ?>
      <?php if ($qq['type'] === 'select'): ?>
        <select name="q[<?= e($key) ?>]" <?= $qq['required'] ? 'required' : '' ?>>
          <option value="">Choose…</option>
          <?php foreach ($qq['options'] as $opt): ?><option <?= $val === $opt ? 'selected' : '' ?>><?= e($opt) ?></option><?php endforeach; ?>
        </select>
      <?php elseif ($qq['type'] === 'date'): ?>
        <input type="date" name="q[<?= e($key) ?>]" value="<?= e($val) ?>">
      <?php else: ?>
        <input name="q[<?= e($key) ?>]" maxlength="<?= (int) ($qq['max'] ?? 200) ?>" value="<?= e($val) ?>">
      <?php endif; ?>
      </label>
    <?php endforeach; ?>
    </div>
  </section>
  <section class="card reveal">
    <h2>3. Details, script and ideas</h2>
    <label>Script / text for the video <small class="opt">(optional)</small><textarea name="script" rows="6" maxlength="20000"><?= e($order['script']) ?></textarea></label>
    <label>Tell us about the video: what it is for, what should be in it, how it should feel <span class="req">*</span><textarea name="ideas" rows="6" minlength="10" maxlength="10000" required placeholder="What is the video about? Which parts to keep or cut, colours, feeling, text on screen, anything else…"><?= e($order['ideas']) ?></textarea></label>
  </section>
  <div class="actions sticky">
    <button class="btn" name="action" value="save" formnovalidate>Save draft</button>
    <button class="btn primary" name="action" value="submit" data-submit>Submit order</button>
  </div>
</form>
<?php foreach ($files as $f): ?>
<form id="del-<?= (int) $f['id'] ?>" method="post" action="<?= e(base_url('orders/' . $order['id'] . '/files/' . $f['id'] . '/delete')) ?>" hidden><?= csrf_field() ?></form>
<?php endforeach; ?>
