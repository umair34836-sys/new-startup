<?php
$title = $order['title'];
$a = order_answers($order);
$latest = $versions[0] ?? null;
$steps = ['submitted' => 'Received', 'in_progress' => 'Editing', 'delivered' => 'Ready', 'approved' => 'Approved'];
$reach = ['submitted' => 0, 'in_progress' => 1, 'revision' => 1, 'delivered' => 2, 'approved' => 3][$order['status']] ?? 0;
?>
<div class="head-row reveal">
  <h1><?= e($order['title']) ?></h1>
  <span class="badge s-<?= e($order['status']) ?>"><?= e(ORDER_STATUSES[$order['status']] ?? '') ?></span>
</div>
<ol class="progress reveal" aria-label="Order progress">
  <?php $i = 0; foreach ($steps as $s => $label): ?>
    <li class="<?= $i <= $reach ? 'done' : '' ?>"><?= e($label) ?></li>
  <?php $i++; endforeach; ?>
</ol>

<?php if ($latest): ?>
<section class="card reveal">
  <h2>Version <?= (int) $latest['number'] ?></h2>
  <?php if (str_starts_with($latest['mime'], 'video/')): ?>
    <video class="player" controls preload="metadata" playsinline src="<?= e(base_url('files/' . $latest['file_id'])) ?>"></video>
  <?php elseif (str_starts_with($latest['mime'], 'image/')): ?>
    <img class="player" alt="Version <?= (int) $latest['number'] ?>" src="<?= e(base_url('files/' . $latest['file_id'])) ?>">
  <?php endif; ?>
  <?php if ($latest['note']): ?><p><?= nl2br(e($latest['note'])) ?></p><?php endif; ?>
  <p><a class="btn" href="<?= e(base_url('files/' . $latest['file_id'] . '/download')) ?>">Download (<?= e(fmt_bytes((int) $latest['size'])) ?>)</a></p>
  <?php if ($order['status'] === 'delivered'): ?>
    <div class="review">
      <h3>Koi changes chahiye? Do you want any changes?</h3>
      <form method="post" action="<?= e(base_url('orders/' . $order['id'] . '/changes')) ?>" class="form">
        <?= csrf_field() ?>
        <textarea name="body" rows="4" required minlength="3" maxlength="10000" placeholder="Example: at 0:12 make the text bigger, use a happier song, cut the last 3 seconds…"></textarea>
        <button class="btn">Send changes</button>
      </form>
      <form method="post" action="<?= e(base_url('orders/' . $order['id'] . '/approve')) ?>" class="form approve">
        <?= csrf_field() ?>
        <button class="btn primary" data-confirm="Approve this version as final?">It's perfect, approve</button>
      </form>
    </div>
  <?php elseif ($order['status'] === 'revision'): ?>
    <p class="notice">We got your changes. <?= e(setting('brand_name')) ?> is working on the next version.<?php if (check_times_text() !== ''): ?> Next check: <?= e(next_check_label()) ?>.<?php endif; ?></p>
  <?php endif; ?>
</section>
<?php else: ?>
<section class="card reveal"><h2>We are on it</h2><p>Your order was received. <?= e(setting('promise_text')) ?> The finished video will appear here, and you can ask for changes until it is perfect.</p>
  <?php if ($order['status'] === 'submitted' && check_times_text() !== ''): ?><p class="check-note"><?= e(check_times_text()) ?> Next check: <?= e(next_check_label()) ?>.</p><?php endif; ?></section>
<?php endif; ?>

<?php if (count($versions) > 1): ?>
<section class="card reveal"><h2>Earlier versions</h2><ul class="file-list">
  <?php foreach (array_slice($versions, 1) as $v): ?>
    <li><span class="fname">Version <?= (int) $v['number'] ?> · <?= e(fmt_date($v['created_at'])) ?></span>
      <a href="<?= e(base_url('files/' . $v['file_id'])) ?>">Watch</a> <a href="<?= e(base_url('files/' . $v['file_id'] . '/download')) ?>">Download</a></li>
  <?php endforeach; ?>
</ul></section>
<?php endif; ?>

<section class="card reveal">
  <h2>Messages</h2>
  <ul class="thread">
    <?php foreach ($messages as $msg): ?>
      <li class="msg <?= $msg['sender'] === 'client' ? 'me' : 'them' ?>">
        <span class="who"><?= $msg['sender'] === 'client' ? 'You' : e(setting('brand_name')) ?> · <?= e(fmt_date($msg['created_at'])) ?></span>
        <?= nl2br(e($msg['body'])) ?>
      </li>
    <?php endforeach; ?>
  </ul>
  <?php if ($order['status'] !== 'approved'): ?>
  <form method="post" action="<?= e(base_url('orders/' . $order['id'] . '/message')) ?>" class="form inline">
    <?= csrf_field() ?>
    <textarea name="body" rows="2" required maxlength="10000" placeholder="Write a message…"></textarea>
    <button class="btn">Send</button>
  </form>
  <?php endif; ?>
</section>

<?php if ($order['status'] !== 'approved'): ?>
<section class="card reveal">
  <h2>Add more files</h2>
  <div class="drop" data-uploader data-order="<?= (int) $order['id'] ?>" data-kind="input" data-reload="1" tabindex="0">
    <input type="file" id="pick" multiple>
    <label for="pick" class="btn">Choose files</label><span>or drop them here</span>
  </div>
  <ul class="file-list" data-file-list></ul>
</section>
<?php endif; ?>

<details class="card reveal">
  <summary>Your order details</summary>
  <dl class="details">
    <dt>Length</dt><dd><?= (int) $order['length_sec'] ?> seconds</dd>
    <dt>Price</dt><dd><?= e(fmt_money((float) ($order['final_price'] ?? $order['estimate']), $order['currency'])) ?><?= $order['final_price'] === null ? ' (estimate)' : '' ?></dd>
    <?php foreach (questions() as $k => $qq): if (($a[$k] ?? '') === '') continue; ?>
      <dt><?= e($qq['label']) ?></dt><dd><?= e($a[$k]) ?></dd>
    <?php endforeach; ?>
    <?php if ($order['script']): ?><dt>Script</dt><dd><?= nl2br(e($order['script'])) ?></dd><?php endif; ?>
    <?php if ($order['ideas']): ?><dt>Ideas</dt><dd><?= nl2br(e($order['ideas'])) ?></dd><?php endif; ?>
    <dt>Files</dt><dd><?php foreach ($files as $f) if ($f['kind'] === 'input') echo e($f['orig_name']) . ' (' . e(fmt_bytes((int) $f['size'])) . ')<br>'; ?></dd>
  </dl>
</details>
