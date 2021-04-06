# How to manually create a debian package

Debian wiki: https://wiki.debian.org/DebianRepository

## Create a private/public key pair

Create keys:
gpg --gen-key
Export public key:
gpg --armor --export max@gmail.com > /path/to/folder/max@gmail.com.gpg.key

## Create debian packge

# Binary packages require uppercase...
mkdir -p hello_niko_deb/DEBIAN
mkdir -p -m755 hello_niko_deb/usr/share/doc/hello-niko-runner
mkdir -p -m755 hello_niko_deb/usr/bin
objcopy --strip-debug --strip-unneeded hello_niko_runner
chmod 0555 hello_niko_runner
cp hello_niko_runner hello_niko_deb/usr/bin
dch --create -v 0.1-1 --package hello-niko-runner
gzip --best changelog
mv changelog.gz hello_niko_runner/usr/share
touch hello_niko_deb/DEBIAN/control

## Build debian package

fakeroot dpkg-deb --build hello_niko_deb .
or
fakeroot dpkg-deb --build hello_niko_deb helloniko.deb

sign package (optional)
dpkg-sig --sign builder helloniko.deb

## Check quality of debian package

lintian hello_niko_runner.deb

## Install/Remove debian package

dpkg --install helloniko.deb
dpkg --remove helloniko