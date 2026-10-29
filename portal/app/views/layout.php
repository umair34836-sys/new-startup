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
<meta name="theme-color" content="#0f172a">
<link rel="manifest" href="<?= e(base_url('manifest.webmanifest')) ?>">
<link rel="icon" href="<?= e(base_url('assets/icons/icon-192.png')) ?>">
<link rel="apple-touch-icon" href="<?= e(base_url('assets/icons/icon-192.png')) ?>">
<link rel="stylesheet" href="<?= e(base_url('assets/app.css')) ?>?v=1">
<script src="<?= e(base_url('assets/vendor/gsap-3.14.2.min.js')) ?>" defer></script>
<script src="<?= e(base_url('assets/app.js')) ?>?v=1" defer></script>
</head>
<body data-csrf="<?= e(csrf_token()) ?>" data-base="<?= e(rtrim(base_url(''), '/')) ?>">
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
<footer class="foot">© <?= date('Y') ?> <?= e($brand) ?></footer>
</body>
</html>
