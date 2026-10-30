<?php $title = 'Account'; ?>
<section class="card narrow reveal">
  <h1>Account</h1>
  <p><strong><?= e($user['name']) ?></strong><br><?= e($user['email']) ?><?php if ($user['phone']): ?><br><?= e($user['phone']) ?><?php endif; ?></p>
  <p class="muted">Currency: <?= e($user['currency']) ?> · Rate: <?= e(fmt_money(rate_for($user, $user['currency']), $user['currency'])) ?> per second of finished video</p>
  <h2>Change password</h2>
  <?php if ($msg): ?><p class="notice <?= e($msg[0]) ?>"><?= e($msg[1]) ?></p><?php endif; ?>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <label>Current password<input name="current" type="password" required autocomplete="current-password"></label>
    <label>New password (8+ characters)<input name="new" type="password" required minlength="8" autocomplete="new-password"></label>
    <button class="btn">Change password</button>
  </form>
</section>
