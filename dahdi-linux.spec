#
# TODO:
# - IMPORTANT rename: http://www.asterisk.org/zaptel-to-dahdi
# - Fix --without xpp:
#   + check_modules
#   unpackaged module: drivers/dahdi/xpp/xpd_bri
#   unpackaged module: drivers/dahdi/xpp/xpd_fxo
#   unpackaged module: drivers/dahdi/xpp/xpd_fxs
#   unpackaged module: drivers/dahdi/xpp/xpd_pri
#   unpackaged module: drivers/dahdi/xpp/xpp
#   unpackaged module: drivers/dahdi/xpp/xpp_usb
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_with	oslec		# with Open Source Line Echo Canceller
%bcond_without	xpp		# without Astribank
%bcond_without	userspace	# don't build userspace packages
%bcond_with	verbose

%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%ifarch sparc
%undefine	with_smp
%endif
%ifarch alpha
%undefine	with_xpp
%endif

%define		rel	3
%define		pname	dahdi-linux
%define		FIRMWARE_URL http://downloads.digium.com/pub/telephony/firmware/releases
Summary:	DAHDI telephony device support
Summary(pl.UTF-8):	Obsługa urządzeń telefonicznych DAHDI
Name:		%{pname}%{_alt_kernel}
Version:	2.3.0
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://downloads.digium.com/pub/telephony/dahdi-linux/dahdi-linux-%{version}.tar.gz
# Source0-md5:	2c26fc3ad3db731f1793a0fc638f1985
Source3:	%{FIRMWARE_URL}/dahdi-fw-oct6114-064-1.05.01.tar.gz
# Source3-md5:	88db9b7a07d8392736171b1b3e6bcc66
Source4:	%{FIRMWARE_URL}/dahdi-fw-oct6114-128-1.05.01.tar.gz
# Source4-md5:	c1f1a18d3e20d283f42c71e580a64b5a
Source5:	%{FIRMWARE_URL}/dahdi-fw-vpmadt032-1.07.tar.gz
# Source5-md5:	e1c7231d6225ac999cb18f4e858f66b6
Source6:	%{FIRMWARE_URL}/dahdi-fw-tc400m-MR6.12.tar.gz
# Source6-md5:	2ea860bb8a9d8ede2858b9557b74ee3c
Source7:	%{FIRMWARE_URL}/dahdi-fw-hx8-2.06.tar.gz
# Source7-md5:	a7f3886942bb3e9fed349a41b3390c9f
Patch0:		%{pname}-dummy.patch
URL:		http://www.asterisk.org/
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build
%endif
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Rules:
# - modules_X: single modules, just name module with no suffix
# - modules_X: subdir modules are just directory name with slash like dirname/
# - keep X and X_in in sync
# - X is used for actual building (entries separated with space), X_in for pld macros (entries separated with comma)

%define	modules_1	dahdi.o dahdi_dynamic.o dahdi_dynamic_eth.o dahdi_dynamic_ethmf.o dahdi_dynamic_loc.o dahdi_dummy.o dahdi_echocan_jpah.o dahdi_echocan_kb1.o dahdi_echocan_mg2.o dahdi_echocan_sec.o dahdi_echocan_sec2.o pciradio.o tor2.o wcfxo.o wct1xxp.o wctdm.o wcte11xp.o
%define	modules_1_in	dahdi,dahdi_dynamic,dahdi_dynamic_eth,dahdi_dynamic_ethmf,dahdi_dynamic_loc,dahdi_dummy,dahdi_echocan_jpah,dahdi_echocan_kb1,dahdi_echocan_mg2,dahdi_echocan_sec,dahdi_echocan_sec2,pciradio,tor2,wcfxo,wct1xxp,wctdm,wcte11xp
%define	modules_2	voicebus/ wct4xxp/ wcte12xp/ %{?with_xpp:xpp/}
%define	modules_2_in	voicebus/dahdi_voicebus,wct4xxp/wct4xxp,wcte12xp/wcte12xp,%{?with_xpp:xpp/xpd_bri,xpp/xpd_fxo,xpp/xpd_fxs,xpp/xpd_pri,xpp/xpp,xpp/xpp_usb}
%ifnarch alpha
%define	modules_nalpha	wctc4xxp/ wctdm24xxp/ dahdi_transcode.o wcb4xxp/
%define	modules_nalpha_in	wctc4xxp/wctc4xxp,wctdm24xxp/wctdm24xxp,dahdi_transcode,wcb4xxp/wcb4xxp
%endif
%define	modules		%{modules_1} %{modules_2}%{?modules_nalpha: %{modules_nalpha}}
%define	modules_in	%{modules_1_in},%{modules_2_in}%{?modules_nalpha:,%{modules_nalpha_in}}

%description
DAHDI telephony device driver.

%description -l pl.UTF-8
Sterownik do urządzeń telefonicznych DAHDI.

%package devel
Summary:	Header files for dahdi interface
Group:		Development/Libraries
# if base package contains shared library for which these headers are
#Requires:	%{name} = %{version}-%{release}
# if -libs package contains shared library for which these headers are
#Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for dahdi interface.

%package udev
Summary:	udev rules for DAHDI kernel modules
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla DAHDI
Release:	%{rel}
Group:		Base/Kernel
Requires:	dahdi-tools >= 2.2.0
Requires:	udev-core

%description udev
udev rules for DAHDI kernel modules.

%description udev -l pl.UTF-8
Reguły udev dla modułów jądra Linuksa dla DAHDI.

%package -n kernel%{_alt_kernel}-%{pname}
Summary:	DAHDI Linux kernel driver
Summary(pl.UTF-8):	Sterownik DAHDI dla jądra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%{?with_oslec:Requires:	kernel-misc-oslec = 20070608-0.1@%{_kernel_ver_str}}
%endif

%description -n kernel%{_alt_kernel}-%{pname}
DAHDI telephony Linux kernel driver.

%description -n kernel%{_alt_kernel}-%{pname} -l pl.UTF-8
Sterownik dla jądra Linuksa do urządzeń telefonicznych DAHDI.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

for a in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7}; do
	ln -s $a drivers/dahdi/firmware
	tar -C drivers/dahdi/firmware -xzf $a
done

cat > download-logger <<'EOF'
#!/bin/sh
# keep log of files make wanted to download in firmware/ dir
echo "$@" >> download.log
EOF
chmod a+rx download-logger

%build
%{__make} include/dahdi/version.h

%build_kernel_modules SUBDIRS=$PWD/drivers/dahdi DAHDI_BUILD_ALL=m HOTPLUG_FIRMWARE=yes DAHDI_MODULES_EXTRA=" " -m %{modules_in} KSRC=$PWD/o -C drivers/dahdi DAHDI_INCLUDE=$PWD/../../include

check_modules() {
	err=0
	for a in drivers/dahdi/{*/,}*.ko; do
		[[ $a = *-dist.ko ]] && continue
		[[ $a = *-up.ko ]] && continue
		[[ $a = *-smp.ko ]] && continue
		echo >&2 "unpackaged module: ${a%.ko}"
		err=1
	done

	[ $err = 0 ] || exit 1
}
check_modules

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%{_includedir}/dahdi -p
cd drivers/dahdi
%install_kernel_modules -m %{modules_in} -d misc
cd ../..

%if %{with userspace}
install -d $RPM_BUILD_ROOT/etc/udev/rules.d

%{make} \
	DESTDIR=$RPM_BUILD_ROOT \
	install-devices \
	install-include
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-%{pname}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-%{pname}
%depmod %{_kernel_ver}

%if %{with userspace}
%files devel
%defattr(644,root,root,755)
%{_includedir}/dahdi

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/dahdi.rules
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/xpp.rules
%endif

%files -n kernel%{_alt_kernel}-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
