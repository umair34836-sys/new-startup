<?php $title = 'Log in'; ?>
<section class="card narrow reveal">
  <h1>Log in</h1>
  <?php if ($error): ?><p class="notice err" role="alert"><?= e($error) ?></p><?php endif; ?>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <label>Email<input name="email" type="email" required autocomplete="email" value="<?= e($email) ?>"></label>
    <label>Password<input name="password" type="password" required autocomplete="current-password"></label>
    <button class="btn primary">Log in</button>
  </form>
  <p class="muted">New here? <a href="<?= e(base_url('register')) ?>">Create an account</a></p>
</section>
