[app]
title = Bullet Knight
package.name = bulletknight
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg

version = 1.0

requirements = kivy

orientation = landscape
fullscreen = 1

android.permissions = INTERNET
android.minapi = 21
android.sdk = 33

android.sdk_path = /home/runner/android-sdk
android.accept_sdk_license = True
android.skip_update = True

[buildozer]
log_level = 2
android.api = 33
android.build_tools = 33.0.0
