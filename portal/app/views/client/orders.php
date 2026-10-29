<?php $title = 'My videos'; ?>
<div class="head-row reveal">
  <h1>My videos</h1>
  <form method="post" action="<?= e(base_url('orders/new')) ?>"><?= csrf_field() ?><button class="btn primary">+ New video order</button></form>
</div>
<?php if (!$orders): ?>
  <section class="card empty reveal"><h2>No orders yet</h2><p>Start a new order: upload your footage and tell us how you want it edited. <?= e(setting('promise_text')) ?></p></section>
<?php else: ?>
  <ul class="order-list stagger">
  <?php foreach ($orders as $o): ?>
    <li class="card order-item">
      <a href="<?= e(base_url('orders/' . $o['id'])) ?>">
        <span class="title"><?= e($o['title']) ?></span>
        <span class="badge s-<?= e($o['status']) ?>"><?= e(ORDER_STATUSES[$o['status']] ?? $o['status']) ?></span>
        <span class="meta">#<?= (int) $o['id'] ?> · <?= (int) $o['length_sec'] ?> s · <?= e(fmt_money((float) ($o['final_price'] ?? $o['estimate']), $o['currency'])) ?> · <?= e(fmt_date($o['updated_at'])) ?></span>
      </a>
    </li>
  <?php endforeach; ?>
  </ul>
<?php endif; ?>
