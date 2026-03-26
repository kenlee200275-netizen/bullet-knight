name: Build APK

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Install system deps
      run: |
        sudo apt update
        sudo apt install -y python3-pip git zip unzip openjdk-17-jdk wget

    - name: Install buildozer
      run: |
        pip install buildozer cython

    - name: Install Android SDK
      run: |
        mkdir -p
