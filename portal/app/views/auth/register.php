<?php $title = 'Create account'; ?>
<section class="card narrow reveal">
  <h1>Create your account</h1>
  <p class="promise"><?= e(setting('promise_text')) ?></p>
  <?php foreach ($errors as $er): ?><p class="notice err" role="alert"><?= e($er) ?></p><?php endforeach; ?>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <label>Your name<input name="name" required maxlength="120" autocomplete="name" value="<?= e($old['name'] ?? '') ?>"></label>
    <label>Email<input name="email" type="email" required autocomplete="email" value="<?= e($old['email'] ?? '') ?>"></label>
    <label>WhatsApp / phone <small>(optional)</small><input name="phone" maxlength="40" autocomplete="tel" value="<?= e($old['phone'] ?? '') ?>"></label>
    <label>Currency
      <select name="currency">
        <option value="PKR" <?= ($old['currency'] ?? '') === 'USD' ? '' : 'selected' ?>>PKR (Pakistani Rupee)</option>
        <option value="USD" <?= ($old['currency'] ?? '') === 'USD' ? 'selected' : '' ?>>USD (US Dollar)</option>
      </select></label>
    <label>Password <small>(8+ characters)</small><input name="password" type="password" required minlength="8" autocomplete="new-password"></label>
    <button class="btn primary">Create account</button>
  </form>
  <p class="muted">Have an account? <a href="<?= e(base_url('login')) ?>">Log in</a></p>
</section>
