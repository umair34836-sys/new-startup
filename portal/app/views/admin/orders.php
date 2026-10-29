<?php $title = 'Orders'; ?>
<div class="head-row reveal"><h1>Orders</h1>
  <span class="muted"><?= (int) $pending ?> open bridge event(s)</span></div>
<nav class="tabs reveal">
  <a href="<?= e(base_url('admin')) ?>" class="<?= $status === '' ? 'on' : '' ?>">All</a>
  <?php foreach (ORDER_STATUSES as $k => $label): ?>
    <a href="<?= e(base_url('admin?status=' . $k)) ?>" class="<?= $status === $k ? 'on' : '' ?>"><?= e($label) ?> (<?= (int) ($counts[$k] ?? 0) ?>)</a>
  <?php endforeach; ?>
</nav>
<table class="table reveal">
  <thead><tr><th>#</th><th>Video</th><th>Client</th><th>Status</th><th>Length</th><th>Price</th><th>Updated</th></tr></thead>
  <tbody class="stagger">
  <?php foreach ($orders as $o): ?>
    <tr>
      <td><?= (int) $o['id'] ?></td>
      <td><a href="<?= e(base_url('admin/orders/' . $o['id'])) ?>"><?= e($o['title']) ?></a></td>
      <td><?= e($o['client_name']) ?><br><small class="muted"><?= e($o['client_email']) ?></small></td>
      <td><span class="badge s-<?= e($o['status']) ?>"><?= e(ORDER_STATUSES[$o['status']] ?? $o['status']) ?></span></td>
      <td><?= (int) $o['length_sec'] ?> s</td>
      <td><?= e(fmt_money((float) ($o['final_price'] ?? $o['estimate']), $o['currency'])) ?></td>
      <td><?= e(fmt_date($o['updated_at'])) ?></td>
    </tr>
  <?php endforeach; ?>
  <?php if (!$orders): ?><tr><td colspan="7" class="muted">No orders.</td></tr><?php endif; ?>
  </tbody>
</table>
