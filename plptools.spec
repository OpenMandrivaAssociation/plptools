%define version 1.0.6
%define rel 2
%define release %mkrel %rel

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
Version: %{version}
Release: %{release}
URL: http://plptools.sourceforge.net/
Source: http://downloads.sourceforge.net/plptools/plptools-%{version}.tar.gz
Patch0: plptools-0.17-lib64.patch
Patch1: plptools-0.18-init_lsb.patch
Patch2: plptools-fix-format-not-a-string-literal.patch
License: GPL
Group: Communications
Buildrequires: readline-devel newt-devel termcap-devel kdelibs-devel >= 2.1
BuildRequires: fuse-devel
Requires: chkconfig >= 0.9
Requires(post,preun):	rpm-helper
BuildRoot: %{_tmppath}/%{name}-buildroot

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
%patch2 -p1 -b .format-not-a-string-literal

%build
export CPPFLAGS="-D_FILE_OFFSET_BITS=64"
%configure2_5x --with-initdir=%{_initrddir} %{_with_debug} --disable-rpath
%make

%install
rm -Rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/%{_prefix} $RPM_BUILD_ROOT%{_initrddir}
%makeinstall_std
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat>$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/plptools<<EOF
START_NCPD=yes
PLPFUSE_ARGS=
START_PLPFUSE=yes
PLPNFSD_ARGS=
START_PLPPRINTD=yes
PLPPRINTD_ARGS=
EOF

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
test ! -d /mnt/psion && mkdir -p /mnt/psion
%_post_service %{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%preun
%_preun_service %{name}

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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
%{_libdir}/libplp.la
%{_includedir}/%{name}/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libplp.a

