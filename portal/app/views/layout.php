<?php
$brand = (function () { try { return setting('brand_name'); } catch (Throwable) { return 'Portal'; } })();
$u = (function () { try { return current_user(); } catch (Throwable) { return null; } })();
$flash = flash();
$title = $title ?? $brand;
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title><?= e($title) ?> · <?= e($brand) ?></title>
<meta name="theme-color" content="#120b2b">
<link rel="manifest" href="<?= e(base_url('manifest.webmanifest')) ?>">
<link rel="icon" href="<?= e(base_url('assets/icons/icon-192.png')) ?>">
<link rel="apple-touch-icon" href="<?= e(base_url('assets/icons/icon-192.png')) ?>">
<link rel="stylesheet" href="<?= e(base_url('assets/app.css')) ?>?v=1">
<script src="<?= e(base_url('assets/vendor/gsap-3.14.2.min.js')) ?>" defer></script>
<script src="<?= e(base_url('assets/app.js')) ?>?v=1" defer></script>
</head>
<body data-app-notes="<?= e((function () { try { return setting('app_notes'); } catch (Throwable) { return ''; } })()) ?>" data-app-version="<?= (int) (function () { try { return setting('app_version'); } catch (Throwable) { return 0; } })() ?>" data-csrf="<?= e(csrf_token()) ?>" data-base="<?= e(rtrim(base_url(''), '/')) ?>">
<div class="splash" id="splash" hidden aria-hidden="true">
  <div class="splash-logo">
    <img class="splash-mark" src="<?= e(base_url('assets/icons/logo-480.png')) ?>" alt="" width="240" height="240">
    <svg class="splash-ring" viewBox="0 0 200 200" width="240" height="240"><defs><linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00d4b8"/><stop offset="1" stop-color="#f5a623"/></linearGradient></defs><circle cx="100" cy="100" r="75.5" fill="none" stroke="url(#ringGrad)" stroke-width="9" stroke-linecap="round"/></svg>
  </div>
  <div class="splash-word"><?= e($brand) ?></div>
  <div class="splash-sub"><?= e((function () { try { return setting('splash_subtitle'); } catch (Throwable) { return 'Editor'; } })()) ?></div>
  <div class="splash-host"><?= e(preg_replace('/[^a-z0-9.:-]/i', '', (string) ($_SERVER['HTTP_HOST'] ?? ''))) ?></div>
</div>
<header class="top">
  <a class="brand" href="<?= e(base_url('')) ?>"><img src="<?= e(base_url('assets/icons/logo.png')) ?>" alt="" width="32" height="32"><span><?= e($brand) ?></span></a>
  <?php if ($u): ?>
  <nav>
    <?php if ($u['role'] === 'admin'): ?>
      <a href="<?= e(base_url('admin')) ?>">Orders</a>
      <a href="<?= e(base_url('admin/clients')) ?>">Clients</a>
      <a href="<?= e(base_url('admin/settings')) ?>">Settings</a>
    <?php else: ?>
      <a href="<?= e(base_url('orders')) ?>">My videos</a>
      <a href="<?= e(base_url('account')) ?>">Account</a>
    <?php endif; ?>
    <form method="post" action="<?= e(base_url('logout')) ?>"><?= csrf_field() ?><button class="link">Log out</button></form>
  </nav>
  <?php endif; ?>
</header>
<main class="page" id="main">
<?php if ($flash): ?><p class="notice <?= e($flash['type']) ?>" role="status"><?= e($flash['msg']) ?></p><?php endif; ?>
<?= $content ?>
</main>
<footer class="foot">© <?= date('Y') ?> <?= e($brand) ?> · <a href="<?= e(base_url('privacy')) ?>">Privacy</a></footer>
</body>
</html>
