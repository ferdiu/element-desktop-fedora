# element-desktop-fedora

RPM packaging for [Element Desktop](https://element.io) targeting Fedora via
[COPR](https://copr.fedorainfracloud.org/coprs/ferdiu/element-desktop/).

A GitHub Actions workflow runs daily, polls [element-hq/element-web](https://github.com/element-hq/element-web)
for new release tags, and triggers a fresh COPR build automatically when a new
version is detected. The pre-built binaries are downloaded directly from
[packages.element.io](https://packages.element.io).

Supports **x86_64** and **aarch64**.

## Install

```bash
sudo dnf copr enable ferdiu/element-desktop
sudo dnf install element-desktop
```

## COPR build status

[![element-desktop build](https://copr.fedorainfracloud.org/coprs/ferdiu/element-desktop/package/element-desktop/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ferdiu/element-desktop/package/element-desktop/)

## Workflow status

[![COPR CI build](https://github.com/ferdiu/element-desktop-fedora/actions/workflows/copr-ci.yml/badge.svg)](https://github.com/ferdiu/element-desktop-fedora/actions/workflows/copr-ci.yml)

## Tracked version

| Package | Upstream latest |
|---------|----------------|
| element-desktop | [![element-desktop](https://img.shields.io/badge/element--desktop-1.12.22-blue)](https://github.com/element-hq/element-web/releases) |

## Repository structure

```
element-desktop-fedora/
├── element-desktop.spec          # RPM spec file
├── sources/                      # Downloaded tarballs (git-ignored)
└── .github/
    └── workflows/
        └── copr-ci.yml           # Daily CI: version check + COPR build trigger
```

## How it works

1. Every night at 02:00 UTC the workflow runs `git ls-remote` against
   `element-hq/element-web` to find the latest semver tag.
2. It compares that tag against the version currently built in COPR using
   `copr-cli get-package`.
3. If upstream is ahead (or if no COPR build exists yet), it patches the
   version into `element-desktop.spec`, verifies both architecture tarballs
   are available at `packages.element.io`, downloads them via `spectool`,
   builds a source RPM, and submits it to COPR.
4. COPR then builds the final binary RPMs for `x86_64` and `aarch64` across
   all enabled Fedora releases.
5. The README badge table is updated and committed back to the repository.

## Secrets required

Add the following secrets to the repository
(**Settings → Secrets and variables → Actions**):

| Secret | Description |
|--------|-------------|
| `COPR_BUILD_L` | `login` field from your [COPR API token](https://copr.fedorainfracloud.org/api) config |
| `COPR_BUILD_T` | `token` field from your [COPR API token](https://copr.fedorainfracloud.org/api) config |

## Manual trigger

You can trigger the workflow manually from the **Actions** tab. Enable the
**"Force rebuild"** option to bypass the version comparison and rebuild
unconditionally (useful after spec file changes).

## Notes on licensing

Element Desktop bundles Electron, which includes Chromium and a
`libffmpeg.so` containing proprietary codecs. This is standard for the
official Element binary distribution but means the package cannot be
submitted to the official Fedora repositories. COPR does not enforce this
restriction, so the package is distributed there instead.

## Author

Federico Manzella — [ferdiu](https://github.com/ferdiu)
