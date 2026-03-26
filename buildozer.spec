[app]
title = Bullet Knight
package.name = bulletknight
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg

version = 1.0

requirements = python3,kivy

orientation = landscape
fullscreen = 1

android.permissions = INTERNET

# 🔥 стабильные версии
android.api = 30
android.minapi = 21
android.ndk = 25b

# не трогаем SDK руками
android.skip_update = False

[buildozer]
log_level = 2
