<div align="center">

# Token2 Arch-Linux app builds
[![Release](https://img.shields.io/github/v/release/gabgutf/token2-aur)](https://github.com/gabgutf/token2-aur/releases)
[![Continuous Integration](https://github.com/gabgutf/token2-aur/actions/workflows/ci.yml/badge.svg)](https://github.com/gabgutf/token2-aur/actions/workflows/ci.yml)

</div>

This repository contains `PKGBUILD`s for Token2's [fido2-manage](https://github.com/token2/fido2-manage) suite of apps. These include `token2-key-manager`, a GUI for managing Token2 hardware keys (packaged as `token2-piv-gui`); as well as `token2-piv-tool`, a CLI version of the same tool.

> [!CAUTION]
> I am not affiliated with Token2, nor is this repository endorsed by them. This repository exists in hope of assisting others, but I am not responsible for any bugs, or hardware issues you may encounter.

## Installation

Since AUR registration is [currently closed](https://aur.archlinux.org/register), you'll have install the packages manually from this repository using `makepkg`.

Keep in mind that the order of installation **must** be the following:

1. `token2-piv-lib`
2. `token2-piv-tool`
3. `token2-piv-gui`

As the latter packages depend on the former.

---

To compile the apps from source, go to the [releases](https://github.com/gabgutf/token2-aur/releases) tab, and download the following files:

- `PKGBUILD-lib`
- `PKGBUILD-tool`
- `PKGBUILD-gui`

Go into your download directory, and run

```shell
$ makepkg -sip PKGBUILD-lib
$ makepkg -sip PKGBUILD-tool
$ makepkg -sip PKGBUILD-gui
```

If you only wish to install the CLI tool, skip the `PKGBUILD-gui` file.

---

If you want to skip compilation and instead use prebuilt packages, download these files instead:

- `PKGBUILD-lib-bin`
- `PKGBUILD-tool-bin`
- `PKGBUILD-gui-bin`

Then, import the PGP signing key from [here](release-key.asc), or download it from a keyserver by running:

```shell
$ gpg --recv-keys 39E817D3FD94AB0D1B0471A0F61EC389BD1EAFBC
```

Finally, run these commands to install the three packages:

```shell
$ makepkg -sip PKGBUILD-lib-bin
$ makepkg -sip PKGBUILD-tool-bin
$ makepkg -sip PKGBUILD-gui-bin
```
