<?php
// The installer (open the site once after upload) writes config.php for you.
// This file only shows what config.php contains. Never commit the real config.php.
return [
    'db_driver' => 'mysql',
    'db_host' => 'localhost',
    'db_port' => 3306,
    'db_name' => 'cpaneluser_portal',
    'db_user' => 'cpaneluser_portal',
    'db_pass' => 'change-me',
    'site_url' => 'https://editor.firecraft.fun', // links in emails and app video links
    'base_path' => '',          // '' when the subdomain points at portal/public
    'timezone' => 'Asia/Karachi',
];
