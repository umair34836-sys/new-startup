<?php $title = 'Order #' . $order['id']; $a = order_answers($order); ?>
<div class="head-row reveal">
  <h1>#<?= (int) $order['id'] ?> <?= e($order['title']) ?></h1>
  <span class="badge s-<?= e($order['status']) ?>"><?= e(ORDER_STATUSES[$order['status']] ?? '') ?></span>
</div>
<div class="grid2">
<section class="card reveal">
  <h2>Client</h2>
  <p><?= e($order['client_name']) ?><br><?= e($order['client_email']) ?><?php if ($order['client_phone']): ?><br><?= e($order['client_phone']) ?><?php endif; ?></p>
  <p class="muted">Claude session: <?= $order['claude_session'] ? '<code>' . e($order['claude_session']) . '</code>' : 'not linked yet' ?></p>
  <dl class="details">
    <dt>Length</dt><dd><?= (int) $order['length_sec'] ?> s × <?= e(fmt_money((float) $order['rate'], $order['currency'])) ?> = <?= e(fmt_money((float) $order['estimate'], $order['currency'])) ?></dd>
    <?php foreach (questions() as $k => $qq): if (($a[$k] ?? '') === '') continue; ?>
      <dt><?= e($qq['label']) ?></dt><dd><?= e($a[$k]) ?></dd>
    <?php endforeach; ?>
    <?php if ($order['script']): ?><dt>Script</dt><dd><?= nl2br(e($order['script'])) ?></dd><?php endif; ?>
    <?php if ($order['ideas']): ?><dt>Ideas</dt><dd><?= nl2br(e($order['ideas'])) ?></dd><?php endif; ?>
  </dl>
  <form method="post" action="<?= e(base_url('admin/orders/' . $order['id'] . '/price')) ?>" class="form inline">
    <?= csrf_field() ?>
    <label>Final price (<?= e($order['currency']) ?>)<input name="final_price" type="number" step="0.01" min="0" value="<?= e((string) ($order['final_price'] ?? '')) ?>"></label>
    <button class="btn">Save price</button>
  </form>
  <form method="post" action="<?= e(base_url('admin/orders/' . $order['id'] . '/status')) ?>" class="form inline">
    <?= csrf_field() ?>
    <label>Status<select name="status"><?php foreach (ORDER_STATUSES as $k => $label): ?><option value="<?= e($k) ?>" <?= $k === $order['status'] ? 'selected' : '' ?>><?= e($label) ?></option><?php endforeach; ?></select></label>
    <button class="btn">Set status</button>
  </form>
</section>
<section class="card reveal">
  <h2>Files</h2>
  <ul class="file-list">
  <?php foreach ($files as $f): ?>
    <li><span class="badge"><?= e($f['kind']) ?></span><span class="fname"><?= e($f['orig_name']) ?></span><span class="muted"><?= e(fmt_bytes((int) $f['size'])) ?></span>
      <a href="<?= e(base_url('files/' . $f['id'] . '/download')) ?>">Download</a></li>
  <?php endforeach; ?>
  </ul>
  <h3>Deliver a version yourself</h3>
  <div class="drop" data-uploader data-order="<?= (int) $order['id'] ?>" data-kind="output" data-reload="1" tabindex="0">
    <input type="file" id="pick"><label for="pick" class="btn">Upload finished file</label>
  </div>
  <ul class="file-list" data-file-list></ul>
  <?php $outs = array_filter($files, fn($f) => $f['kind'] === 'output'); if ($outs): ?>
  <form method="post" action="<?= e(base_url('admin/orders/' . $order['id'] . '/deliver')) ?>" class="form">
    <?= csrf_field() ?>
    <label>File<select name="file_id"><?php foreach (array_reverse($outs) as $f): ?><option value="<?= (int) $f['id'] ?>"><?= e($f['orig_name']) ?></option><?php endforeach; ?></select></label>
    <label>Note to client<textarea name="note" rows="2"></textarea></label>
    <button class="btn primary">Send to client as new version</button>
  </form>
  <?php endif; ?>
</section>
</div>
<section class="card reveal">
  <h2>Versions</h2>
  <ul class="file-list"><?php foreach ($versions as $v): ?><li>Version <?= (int) $v['number'] ?> · <?= e($v['orig_name']) ?> · <?= e(fmt_date($v['created_at'])) ?></li><?php endforeach; ?></ul>
  <h2>Messages</h2>
  <ul class="thread">
    <?php foreach ($messages as $msg): ?>
      <li class="msg <?= $msg['sender'] === 'client' ? 'them' : 'me' ?>"><span class="who"><?= e($msg['sender']) ?> · <?= e($msg['kind']) ?> · <?= e(fmt_date($msg['created_at'])) ?></span><?= nl2br(e($msg['body'])) ?></li>
    <?php endforeach; ?>
  </ul>
  <form method="post" action="<?= e(base_url('admin/orders/' . $order['id'] . '/message')) ?>" class="form inline">
    <?= csrf_field() ?><textarea name="body" rows="2" required></textarea><button class="btn">Send as studio</button>
  </form>
  <h3>Bridge events</h3>
  <ul class="file-list"><?php foreach ($events as $ev): ?><li><?= e($ev['type']) ?> · <?= e(fmt_date($ev['created_at'])) ?> · <?= $ev['done_at'] ? 'done' : ($ev['taken_at'] ? 'taken' : 'waiting') ?></li><?php endforeach; ?></ul>
</section>
