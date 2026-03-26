name: Build APK

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Install deps
      run: |
        sudo apt update
        sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
        pip install buildozer cython

    - name: Build APK
      run: |
        buildozer init || true

        sed -i 's/title = .*/title = BulletKnight/' buildozer.spec
        sed -i 's/package.name = .*/package.name = bulletknight/' buildozer.spec
        sed -i 's/android.api = .*/android.api = 33/' buildozer.spec
        sed -i 's/android.minapi = .*/android.minapi = 21/' buildozer.spec
        sed -i 's/android.sdk = .*/android.sdk = 24/' buildozer.spec
        sed -i 's/android.ndk = .*/android.ndk = 23b/' buildozer.spec

        buildozer android clean
        buildozer
