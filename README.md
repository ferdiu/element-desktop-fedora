# element-desktop-fedora

RPM packaging for [Element Desktop](https://element.io) targeting Fedora via
[COPR](https://copr.fedorainfracloud.org/coprs/ferdiu/element-desktop/).

A GitHub Actions workflow runs daily, polls [element-hq/element-web](https://github.com/element-hq/element-web)
for new release tags, and triggers a fresh COPR build automatically when a new
version is detected. The pre-built binaries are downloaded directly from
[packages.element.io](https://packages.element.io).

Supports **x86\_64** and **aarch64**.

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
| element-desktop | [![element-desktop](https://img.shields.io/badge/element--desktop-1.12.23-blue)](https://github.com/element-hq/element-web/releases) |
