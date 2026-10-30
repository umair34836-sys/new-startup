<?php $title = $title; ?>
<section class="card narrow center reveal">
  <p class="big-code"><?= (int) $code ?></p>
  <h1><?= e($title) ?></h1>
  <?php if ($msg): ?><p><?= e($msg) ?></p><?php endif; ?>
  <p><a class="btn" href="<?= e(base_url('')) ?>">Go home</a></p>
</section>
