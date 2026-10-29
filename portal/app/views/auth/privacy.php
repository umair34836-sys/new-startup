<?php $title = 'Privacy'; ?>
<section class="card narrow reveal">
  <h1>Privacy</h1>
  <p><?= nl2br(e(setting('privacy_text'))) ?></p>
  <?php if (setting('support_contact') !== ''): ?><p class="muted">Contact: <?= e(setting('support_contact')) ?></p><?php endif; ?>
</section>
