<?php $title = 'New password'; ?>
<section class="card narrow reveal">
  <h1>Set a new password</h1>
  <?php if (!$valid): ?>
    <p class="notice err">This link is wrong or expired. <a href="<?= e(base_url('forgot')) ?>">Ask for a new one</a>.</p>
  <?php else: ?>
    <?php if ($error): ?><p class="notice err" role="alert"><?= e($error) ?></p><?php endif; ?>
    <form method="post" action="<?= e(base_url('reset?token=' . rawurlencode($token))) ?>" class="form">
      <?= csrf_field() ?>
      <label>New password (8+ characters)<input name="password" type="password" required minlength="8" autocomplete="new-password"></label>
      <button class="btn primary">Save password</button>
    </form>
  <?php endif; ?>
</section>
