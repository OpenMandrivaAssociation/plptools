%define libmajor 0
%define libname %mklibname plp %libmajor

#
# Conditionals
#
%{?_with_debug: %define _with_debug --enable-debug}
%{?_with_debug: %define optflags -g}
%{!?_with_debug: %define _with_debug --disable-debug}

Summary: Connectivity for psion series 5
Name: plptools
Version: 1.0.11
Release: 3
URL: http://plptools.sourceforge.net/
Source: http://downloads.sourceforge.net/plptools/plptools-%{version}.tar.gz
Patch0: plptools-0.17-lib64.patch
Patch1: plptools-0.18-init_lsb.patch
License: GPL
Group: Communications
Buildrequires: readline-devel newt-devel termcap-devel
BuildRequires: fuse-devel
Requires: chkconfig >= 0.9
Requires(post,preun):	rpm-helper

%description
This package contains the programs (client and server), necessary to
communicate with a Psion palmtop. The psion's file-system will
be automatically mounted under /mnt/psion at the time it is
connected to your computer. If the psion is shut down or
disconnected, the contents of /mnt/psion will automatically
disappear. Other programs included are:
 - plpftp, a program which allows you to transfer files in a ftp-like
   manner, view and modifiy processes on your psion.
 - plpbackup, a backup/restore utility.
 - plpprintd, a daemon for enabling printing from a Psion Series 5 via any
   accessible printer.
 - sisinstall, an installer for Psion's SIS software package format.

%description -l de
Dieses Packet enthält Programme zur Kommunikation mit einem Psion Palmtop.
Das Dateisystem des Psion wird beim Anschließen automatisch unter
/mnt/psion eingehängt. Wird der Psion ausgeschaltet oder das Kabel
gezogen, so verschwindet der Inhalt dieses Verzeichnisses automatisch
und erscheint erneuten Anschließen wieder. Weiterhin sind enthalten:
 - plpftp, ein Programm welches eine FTP-ähnliche Oberfläche für Dateitransfer
   bietet und Prozesse auf dem Psion stoppen und starten kann.
 - plpbackup, ein Backup/Restore Utility für die Kommandozeile.
 - plpprintd, ein Daemon welcher Ausdrucken von einem Psion Serie 5 über
   beliebige vefügbare Drucker ermöglicht
 - sisinstall, ein Installationsprogramm für das Psion-eigene SIS
   packetformat.

%package -n %{libname}
Summary: Shared library for psion series 5 communication
Group: System/Libraries
License: GPL

%description -n %{libname}
This package contains the shared library required by programs which can 
communicate with a Psion palmtop.

%package -n %{libname}-devel
Summary: Development library and headers for psion series 5 communication
Group: Development/C
License: GPL
Provides: plp-devel = %{version}-%{release}
Provides: libplp-devel = %{version}-%{release}
Requires: %{libname} = %{version}

%description -n %{libname}-devel
This package contains the development library and header files for building
programs which can communicate with a Psion palmtop.

%description -l de -n %{libname}-devel
Dieses Packet enthält die statische Bibliothek und include-Dateien
zur Programm-Entwicklung von Kommunikations-software für den Psion.

%package -n %{libname}-static-devel
Summary: Static library for psion series 5 communication
Group: Development/C
License: GPL
Requires: %{libname}-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static library for building programs which can 
communicate with a Psion palmtop.

%prep
%setup -q
#patch0 -p1 -b .lib64
%patch1 -p1 -b .init_lsb

%build
export CPPFLAGS="-D_FILE_OFFSET_BITS=64"
%configure2_5x --with-initdir=%{_initrddir} %{_with_debug} --disable-rpath
%make

%install
mkdir -p %{buildroot}/%{_prefix} $%{buildroot}%{_initrddir}
%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat>%{buildroot}%{_sysconfdir}/sysconfig/plptools<<EOF
START_NCPD=yes
PLPFUSE_ARGS=
START_PLPFUSE=yes
PLPNFSD_ARGS=
START_PLPPRINTD=yes
PLPPRINTD_ARGS=
EOF

%{find_lang} %{name}

%post
test ! -d /mnt/psion && mkdir -p /mnt/psion
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING INSTALL ChangeLog README TODO etc/*magic
%doc etc/udev-usbserial-plptools.rules
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*
%{_datadir}/%{name}/*
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libplp.so.%{libmajor}*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/api
%{_libdir}/libplp.so
%{_includedir}/%{name}/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libplp.a



%changelog
* Wed Oct 20 2010 Buchan Milne <bgmilne@mandriva.org> 1.0.11-1mdv2011.0
+ Revision: 586929
- update to new version 1.0.11

* Mon Sep 06 2010 Buchan Milne <bgmilne@mandriva.org> 1.0.10-1mdv2011.0
+ Revision: 576264
- update to new version 1.0.10

* Wed Jan 06 2010 Buchan Milne <bgmilne@mandriva.org> 1.0.9-1mdv2010.1
+ Revision: 486582
- New version 1.0.9
- update to new version 1.0.8

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Mar 13 2009 Buchan Milne <bgmilne@mandriva.org> 1.0.7-1mdv2009.1
+ Revision: 354625
- New version 1.0.7
- Drop patch2, format-not-a-string-literal fixed upstream

* Fri Feb 27 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.6-2mdv2009.1
+ Revision: 345504
- rebuild against new readline

* Sat Jan 31 2009 Buchan Milne <bgmilne@mandriva.org> 1.0.6-1mdv2009.1
+ Revision: 335772
- New version 1.0.6
-Fix "format not a string literal"

* Mon Jul 28 2008 Buchan Milne <bgmilne@mandriva.org> 1.0.5-1mdv2009.0
+ Revision: 251327
- New version 1.0.5

* Sat Jun 21 2008 Buchan Milne <bgmilne@mandriva.org> 1.0.4-1mdv2009.0
+ Revision: 227811
- New version 1.0.4

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Mar 03 2008 Buchan Milne <bgmilne@mandriva.org> 0.20-1mdv2008.1
+ Revision: 178220
- New version 0.18
- Drop kde subpackages, as kde tools dropped upstream
- Buildrequire fuse-devel

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot

* Fri Aug 10 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.18-1mdv2008.0
+ Revision: 61611
- Changed PreReq for rpm-helper to Requires(post,preun).
- Added LSB support to psion initscript (init_lsb patch).
- Removed use of kdedesktop2mdkmenu.pl, it doesn't exist anymore.
- Updated to version 0.18.
- Run update_icon_cache in scriptlets of kde subpackage, because it
  ships icons for hicolor icon theme.
- Added lib64 patch, quick fix to build with x86_64 (the right fix would
  be update auto-tools files to regenerate configure script, but the
  files are very outdated, in a strange layout, and simply replacing kde
  macro definitions isn't working right now).
- Removed BuildRequires for kdelibs-common, not really needed (already
  installed with kdelibs-devel).
- Added missing BuildRequires for kdelibs-common.
- Updated to version 0.17.
- Minor cleanups.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild for new slang


* Sat Aug 19 2006 Buchan Milne <bgmilne@mandriva.org> 0.15-1mdv2007.0
- 0.15

* Sun Aug 28 2005 Austin ACton <austin@mandriva.org> 0.14-1mdk
- 0.14
- configure 2.5
- minor rpmlint fixes
- drop qt-mt patch

