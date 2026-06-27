# element-desktop.spec
#
# Packages the pre-built Element Desktop Electron binary distributed by Element
# at https://packages.element.io for x86_64 and aarch64.
#
# Version is kept in sync with upstream element-hq/element-web tags.
# The tarball URLs differ between architectures:
#   x86_64  : https://packages.element.io/desktop/install/linux/glibc-x86-64/element-desktop-{VERSION}.tar.gz
#   aarch64 : https://packages.element.io/desktop/install/linux/glibc-aarch64/element-desktop-{VERSION}-arm64.tar.gz

Name:           element-desktop
Version:        1.12.22
Release:        1%{?dist}
Summary:        A glossy Matrix collaboration client for the desktop

License:        AGPL-3.0-or-later AND LicenseRef-Element-Commercial
URL:            https://element.io

# Architecture-specific source tarballs (downloaded by spectool at build time)
%ifarch x86_64
Source0:        https://packages.element.io/desktop/install/linux/glibc-x86-64/element-desktop-%{version}.tar.gz
%endif
%ifarch aarch64
Source0:        https://packages.element.io/desktop/install/linux/glibc-aarch64/element-desktop-%{version}-arm64.tar.gz
%endif

# Element Desktop ships as a self-contained pre-built Electron binary.
# The bundled Electron/Chromium runtime brings its own internals; only the
# libraries listed below must be provided by the OS.
Requires:       gtk3
Requires:       libnotify
Requires:       nss
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       xdg-utils
Requires:       at-spi2-core
Requires:       libuuid
Requires:       libdrm
Requires:       mesa-libgbm
Requires:       alsa-lib
Requires:       libXrandr
Requires:       libXdamage
Requires:       libXcomposite
Requires:       libXfixes

# The tarball is a pre-built binary blob; no compilation takes place.
%global debug_package %{nil}

ExclusiveArch:  x86_64 aarch64

%description
Element (formerly Riot) is a Matrix-protocol collaboration client.
It supports end-to-end encrypted messaging, voice/video calls, file
sharing and extensive bridging to other networks.

This package installs the official pre-built Element Desktop Electron
binary provided by Element at https://packages.element.io.

%prep
%setup -q -c

%build
# Nothing to build — the tarball is already a compiled Electron application.

%install
# Determine the unpacked directory name (varies by arch)
%ifarch x86_64
_srcdir="element-desktop-%{version}"
%endif
%ifarch aarch64
_srcdir="element-desktop-%{version}-arm64"
%endif

install -d %{buildroot}/opt/element-desktop
cp -a "${_srcdir}/." %{buildroot}/opt/element-desktop/

# Launcher wrapper script
install -Dm755 /dev/stdin %{buildroot}%{_bindir}/element-desktop << 'EOF'
#!/bin/sh
exec /opt/element-desktop/element-desktop "$@"
EOF

# Desktop entry
install -Dm644 /dev/stdin \
    %{buildroot}%{_datadir}/applications/element-desktop.desktop << 'EOF'
[Desktop Entry]
Name=Element
GenericName=Matrix Client
Comment=A glossy Matrix collaboration client for the desktop
Exec=element-desktop %U
Icon=element-desktop
Terminal=false
Type=Application
Categories=Network;InstantMessaging;Chat;IRCClient;
MimeType=x-scheme-handler/element;x-scheme-handler/io.element.desktop;
StartupWMClass=Element
EOF

# Icon lives at resources/build/icon.png inside the tarball
install -Dm644 "${_srcdir}/resources/build/icon.png" \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/element-desktop.png

%post
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :

%files
/opt/element-desktop/
%{_bindir}/element-desktop
%{_datadir}/applications/element-desktop.desktop
%{_datadir}/icons/hicolor/256x256/apps/element-desktop.png

%changelog
* Sat Jun 27 2026 Federico Manzella <ferdiu@users.noreply.github.com> - 1.12.22-1
- Initial packaging of Element Desktop for Fedora via COPR
