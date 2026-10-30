<?php $title = 'Welcome'; ?>
<section class="hero reveal">
  <h1><?= e(setting('brand_name')) ?></h1>
  <p class="lead"><?= e(setting('brand_tagline')) ?></p>
  <p class="promise"><?= e(setting('promise_text')) ?></p>
  <?php if (check_times_text() !== ''): ?><p class="check-note"><?= e(check_times_text()) ?></p><?php endif; ?>
  <div class="row">
    <a class="btn primary" href="<?= e(base_url('register')) ?>">Create account</a>
    <a class="btn" href="<?= e(base_url('login')) ?>">Log in</a>
  </div>
  <?php if (is_file(storage_dir() . '/app/app.apk')): ?>
    <p class="app-get"><a class="btn" href="<?= e(base_url('app/download')) ?>" data-app-link>Get the Android app</a></p>
  <?php endif; ?>
</section>
<section class="steps stagger">
  <div class="step card"><span class="num">1</span><h3>Send your footage</h3><p>Upload raw videos, images and your script. Big files are fine.</p></div>
  <div class="step card"><span class="num">2</span><h3>Tell us your idea</h3><p>Answer a few questions: style, music, length, captions, deadline.</p></div>
  <div class="step card"><span class="num">3</span><h3>Review and approve</h3><p>MrCopper804 edits it by hand. Watch it here and ask for changes until it is perfect.</p></div>
</section>
