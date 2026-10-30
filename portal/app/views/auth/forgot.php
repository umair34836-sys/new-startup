<?php $title = 'Forgot password'; ?>
<section class="card narrow reveal">
  <h1>Forgot password</h1>
  <?php if ($sent): ?>
    <p class="notice ok">If an account with that email exists, we sent a link to set a new password. Check your inbox and spam folder.</p>
  <?php else: ?>
    <p class="muted">Enter your email and we will send you a link to set a new password.</p>
    <form method="post" class="form">
      <?= csrf_field() ?>
      <label>Email<input name="email" type="email" required autocomplete="email"></label>
      <button class="btn primary">Send link</button>
    </form>
  <?php endif; ?>
  <p class="muted"><a href="<?= e(base_url('login')) ?>">Back to log in</a></p>
</section>
