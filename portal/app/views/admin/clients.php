<?php $title = 'Clients'; ?>
<h1 class="reveal">Clients</h1>
<p class="muted reveal">Leave a rate empty to use the default rate from Settings (<?= e(setting('rate_pkr')) ?> PKR / <?= e(setting('rate_usd')) ?> USD per second).</p>
<div class="stagger">
<?php foreach ($clients as $c): ?>
  <form method="post" action="<?= e(base_url('admin/clients/' . $c['id'])) ?>" class="card form client-row">
    <?= csrf_field() ?>
    <div><?php if ($c['status'] === 'pending'): ?><span class="badge s-revision">Waiting for approval</span> <?php endif; ?><strong><?= e($c['name']) ?></strong> <span class="muted"><?= e($c['email']) ?> <?= e($c['phone']) ?></span><br>
      <small class="muted"><?= (int) $c['order_count'] ?> orders · joined <?= e(fmt_date($c['created_at'])) ?></small></div>
    <div class="grid4">
      <label>Currency<select name="currency"><option <?= $c['currency'] === 'PKR' ? 'selected' : '' ?>>PKR</option><option <?= $c['currency'] === 'USD' ? 'selected' : '' ?>>USD</option></select></label>
      <label>PKR / second<input name="rate_pkr" type="number" step="0.0001" min="0" value="<?= e((string) ($c['rate_pkr'] ?? '')) ?>"></label>
      <label>USD / second<input name="rate_usd" type="number" step="0.0001" min="0" value="<?= e((string) ($c['rate_usd'] ?? '')) ?>"></label>
      <label>Status<select name="status"><?php foreach (['pending' => 'waiting for approval', 'active' => 'active (approved)', 'blocked' => 'blocked'] as $sv => $sl): ?><option value="<?= $sv ?>" <?= $c['status'] === $sv ? 'selected' : '' ?>><?= $sl ?></option><?php endforeach; ?></select></label>
      <label>Claude session id<input name="claude_session" maxlength="120" pattern="[A-Za-z0-9_-]*" value="<?= e((string) $c['claude_session']) ?>"></label>
      <label>Private note<input name="admin_note" maxlength="2000" value="<?= e((string) $c['admin_note']) ?>"></label>
    </div>
    <button class="btn">Save</button>
  </form>
<?php endforeach; ?>
<?php if (!$clients): ?><p class="muted">No clients yet.</p><?php endif; ?>
</div>
