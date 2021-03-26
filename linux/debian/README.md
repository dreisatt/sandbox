# How to manually create a debian package

Debian wiki: https://wiki.debian.org/DebianRepository

## Create a private/public key pair

Create keys:
gpg --gen-key
Export public key:
gpg --armor --export max@gmail.com > /path/to/folder/max@gmail.com.gpg.key

## Build debian package

dpkg-deb --build hello_niko_deb .
or
dpkg-deb --build hello_niko_deb helloniko.deb
optional:
dpkg-sig --sign builder helloniko.deb

## Install/Remove debian package

dpkg --install helloniko.deb
dpkg --remove helloniko