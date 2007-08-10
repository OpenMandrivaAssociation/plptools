%define version 0.18
%define rel 1
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
Source: http://download.sourceforge.net/plptools/plptools-%{version}.tar.gz
Patch0: plptools-0.17-lib64.patch
Patch1: plptools-0.18-init_lsb.patch
License: GPL
Group: Communications
Buildrequires: readline-devel newt-devel termcap-devel kdelibs-devel >= 2.1
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

%package kde
Summary: Psion support for KDE
Group: Graphical desktop/KDE
License: GPL
Requires: %{name} = %{version}
Provides: kpsion = %{version}-%{release} klipsi = %{version}-%{release}
Obsoletes: kpsion klipsi

%description kde
This package provides support for a new protocol prefix "psion:/" for
KDE. Any KDE application which uses KDE-conforming URLs, can access
files on the Psion. Furthermore, a plugin for Konqueror's file-properties
dialog provides access to Psions proprietary file attributes and information
about the Psion's drives as well as generic machine information.

%description -l de kde
Dieses Packet stellt Unterstützung für eine neues Protokoll-Präfix "psion:/"
für KDE bereit. Jede KDE Anwendung, die KDE-konforme URLs benutzt, kann
damit auf die Dateien eines Psion zugreifen. Weiterhin, liefert ein Plugin
für Konqueror's Datei-Eigenschaften-Dialog Informationen über proprietäre
Psion-Dateiattribute und stellt Informationen zum Gerät sowie seiner
Laufwerke zur Verfügung.

%package -n kpsion
Summary: Psion utility for KDE.
Group: User Interface/Desktops
Requires: %{name} = %{version}

%description -n kpsion
This package contains a KDE utility program for backup, restore and formatting
Psion drives.

%description -l de -n kpsion
Dieses Packet enthält ein KDE Werkzeug zum Backup, Restore und Formatieren
von Psion Laufwerken.

%package -n klipsi
Summary: Psion remote clipboard utility for KDE.
Group: User Interface/Desktops
Requires: %{name} = %{version}

%description -n klipsi
This package contains a KDE utility for using the Psion's remote clipboard
function.

%description -l de -n klipsi
Dieses Packet enthält ein KDE Werkzeug zum Transfer der Zwischenablage
zwischen Psion und Rechner.

%prep
%setup -q
%patch0 -p1 -b .lib64
%patch1 -p1 -b .init_lsb

%build
%configure2_5x --enable-kde --with-initdir=%{_initrddir} %{_with_debug} --disable-rpath
%make kdemoduledir=%_libdir/kde3

%install
rm -Rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/%{_prefix} $RPM_BUILD_ROOT%{_initrddir}
%makeinstall_std kdemoduledir=%_libdir/kde3
install -m 644 conf/kiodoc-update.pl \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/kiodoc-update.pl
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat>$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/psion<<EOF
START_NCPD=yes
NCPD_ARGS=
START_PLPNFSD=no
PLPNFSD_ARGS=
START_PLPPRINTD=yes
PLPPRINTD_ARGS=
EOF

#fix paths in libtool files:
find %{buildroot}/%{_libdir} -name '*.la' -exec perl -pi -e "s|-L${RPM_BUILD_DIR}\S*||g" {} \;

#icons
pushd %{buildroot}/%{_iconsdir}
mkdir {large,mini}
for i in psion_desktop.png klipsi.png
do
	ln -s hicolor/32x32/apps/$i ; ln -s ../hicolor/32x32/apps/$i large/; ln -s ../hicolor/16x16/apps/$i mini/
done
popd

%find_lang %{name}
%find_lang kpsion
%find_lang klipsi
%find_lang libplpprops
cat kpsion.lang klipsi.lang libplpprops.lang > plptools-kde.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
test ! -d /mnt/psion && mkdir -p /mnt/psion
%_post_service psion

%post -n %{libname} -p /sbin/ldconfig

%post kde
%{update_menus}
/sbin/ldconfig
KONQRC=`%{_bindir}/kde-config --expandvars --install config`/konquerorrc
if test -f $KONQRC && grep -q '\[Notification Messages\]' $KONQRC ; then
	cp $KONQRC $KONQRC.$$
	cat $KONQRC.$$ | grep -v "askSaveinode/x-psion-drive=No" | sed \
		-e '/\[Notification Messages\]/a' \
		-e 'askSaveinode/x-psion-drive=No' > $KONQRC && \
	rm -f $KONQRC.$$
else
cat>>$KONQRC<<EOF

[Notification Messages]
askSaveinode/x-psion-drive=No
EOF
fi
%update_icon_cache hicolor

%preun
%_preun_service psion

%preun kde
if [ "$1" = 0 ]
then
	/usr/bin/perl %{_datadir}/%{name}/kiodoc-update.pl -r psion
	KONQRC=`kde-config --expandvars --install config`/konquerorrc
	if test -f $KONQRC ; then
		cp $KONQRC $KONQRC.$$
		grep -v 'askSaveinode/x-psion-drive=' $KONQRC.$$ > $KONQRC && \
		rm -f $KONQRC.$$
	fi
fi

%postun -n %{libname} -p /sbin/ldconfig

%postun kde
/sbin/ldconfig
%{clean_menus}
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING INSTALL CHANGES ChangeLog README TODO etc/*magic patches
%{_bindir}/plpftp
%{_bindir}/plpbackup
%{_bindir}/sisinstall
%{_sbindir}/*
%{_mandir}/*/*
%{_datadir}/%{name}/*
%config(noreplace) %{_initrddir}/psion
%config(noreplace) %{_sysconfdir}/sysconfig/psion

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libplp.so.%{libmajor}*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/api etc/*.spec
%{_libdir}/libplp.so
%{_libdir}/libplp.la
%{_includedir}/%{name}/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libplp.a

%files kde -f plptools-kde.lang
%defattr(-,root,root)
%{_libdir}/kde*/kio_plp.so*
%{_libdir}/kde*/kio_plp.la
%{_libdir}/kde*/libplpprops.so
%{_libdir}/kde*/libplpprops.la
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/services/*
%{_datadir}/icons/*/*/mimetypes/*
%{_datadir}/icons/*/*/devices/*
%{_datadir}/icons/*/*/apps/psion*
%{_datadir}/mimelnk/*/*
%{_datadir}/doc/HTML/*/kioslave/*
%{_datadir}/%{name}/kiodoc-update.pl
%exclude %{_libdir}/kde*/*.a

#%files -n kpsion -f kpsion.lang
#%defattr(-,root,root)
%{_bindir}/kpsion
%{_libdir}/libkpsion.so
%{_libdir}/libkpsion.la
%exclude %{_libdir}/libkpsion.a
%{_datadir}/applnk/*/kpsion*
%{_datadir}/apps/kpsion/*
%{_datadir}/apps/konqueror/*
%{_datadir}/icons/*/*/apps/kpsion*
%{_datadir}/icons/*/*/actions/psion*
%{_datadir}/doc/HTML/*/kpsion

#%files -n klipsi -f klipsi.lang
#%defattr(-,root,root)
%{_bindir}/klipsi
%{_libdir}/klipsi.so*
%{_libdir}/klipsi.la
%exclude %{_libdir}/klipsi.a
%{_datadir}/applnk/*/klipsi*
%{_datadir}/apps/klipsi/*
%{_datadir}/icons/*/*/apps/klipsi*
%{_datadir}/icons/*/*/actions/klipsi*

