#
# TODO:
# - IMPORTANT rename: http://www.asterisk.org/dahdi-to-dahdi
#
# - kernel modules doesn't build
# - should more header files be installed?
# - Installed (but unpackaged) file(s) found:
#   /etc/hotplug/usb/xpp_fxloader
#   /etc/hotplug/usb/xpp_fxloader.usermap
#   /etc/udev/rules.d/xpp.rules
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_with	oslec		# with Open Source Line Echo Canceller
%bcond_with	bristuff	# with bristuff support
%bcond_without	xpp		# without Astribank
%bcond_with	verbose

%ifarch sparc
%undefine	with_smp
%endif
%ifarch alpha
%undefine	with_xpp
%endif

%define		rel	11
%define		pname	dahdi-linux
%define		FIRMWARE_URL http://downloads.digium.com/pub/telephony/firmware/releases
Summary:	DAHDI telephony device support
Summary(pl.UTF-8):	Obsługa urządzeń telefonicznych DAHDI
Name:		%{pname}%{_alt_kernel}
Version:	2.1.0.3
Release:	%{rel}%{?with_bristuff:.bristuff}
License:	GPL
Group:		Base/Kernel
Source0:	http://downloads.digium.com/pub/telephony/dahdi-linux/dahdi-linux-2.1.0.3.tar.gz
# Source0-md5:	4e2a294073a1375b8b3d33bbf4f607fe
Source3:	%{FIRMWARE_URL}/dahdi-fw-oct6114-064-1.05.01.tar.gz
# Source3-md5:	88db9b7a07d8392736171b1b3e6bcc66
Source4:	%{FIRMWARE_URL}/dahdi-fw-oct6114-128-1.05.01.tar.gz
# Source4-md5:	c1f1a18d3e20d283f42c71e580a64b5a
Source5:	%{FIRMWARE_URL}/dahdi-fw-vpmadt032-1.07.tar.gz
# Source5-md5:	e1c7231d6225ac999cb18f4e858f66b6
Source6:	%{FIRMWARE_URL}/dahdi-fw-tc400m-MR6.12.tar.gz
# Source6-md5:	2ea860bb8a9d8ede2858b9557b74ee3c
URL:		http://www.asterisk.org/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build
BuildRequires:	module-init-tools
%endif
BuildRequires:	newt-devel
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_bristuff:Provides:	dahdi(bristuff)}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Rules:
# - modules_X: single modules, just name module with no suffix
# - modules_X: subdir modules are just directory name with slash like dirname/
# - keep X and X_in in sync
# - X is used for actual building (entries separated with space), X_in for pld macros (entries separated with comma)

%define	modules_1	dahdi.o dahdi_dynamic_eth.o dahdi_dynamic_loc.o pciradio.o tor2.o wcfxo.o wct1xxp.o wctdm.o wcte11xp.o dahdi_dummy.o dahdi_dynamic.o dahdi_echocan_jpah.o dahdi_echocan_kb1.o dahdi_echocan_mg2.o dahdi_echocan_sec.o dahdi_echocan_sec2.o
%define	modules_1_in	dahdi,dahdi_dynamic_eth,dahdi_dynamic_loc,pciradio,tor2,wcfxo,wct1xxp,wctdm,wcte11xp,dahdi_dummy,dahdi_dynamic,dahdi_echocan_jpah,dahdi_echocan_kb1,dahdi_echocan_mg2,dahdi_echocan_sec,dahdi_echocan_sec2
%define	modules_2	wct4xxp/ wcte12xp/ %{?with_xpp:xpp/}
%define	modules_2_in	wct4xxp/wct4xxp,wcte12xp/wcte12xp%{?with_xpp:,xpp/{%{?with_bristuff:xpd_bri,}xpd_fxo,xpd_fxs,xpd_pri,xpp,xpp_usb}}
%ifnarch alpha
%define	modules_nalpha	wctc4xxp/ wctdm24xxp/ dahdi_transcode.o wcb4xxp/
%define	modules_nalpha_in	wctc4xxp/wctc4xxp,wctdm24xxp/wctdm24xxp,dahdi_transcode,wcb4xxp/wcb4xxp

%endif
%if %{with bristuff}
%define	modules_bristuff cwain/ qozap/ vzaphfc/ zaphfc/ ztgsm/ opvxa1200.o wcopenpci.o
%define	modules_bristuff_in	cwain/cwain,qozap/qozap,vzaphfc/vzaphfc,zaphfc/zaphfc,ztgsm/ztgsm,opvxa1200,wcopenpci
%endif
%define	modules		%{modules_1} %{modules_2}%{?modules_nalpha: %{modules_nalpha}}%{?modules_bristuff: %{modules_bristuff}}
%define	modules_in	%{modules_1_in},%{modules_2_in}%{?modules_nalpha:,%{modules_nalpha_in}}%{?modules_bristuff:,%{modules_bristuff_in}}

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

for a in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
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

install include/dahdi/*.h $RPM_BUILD_ROOT%{_includedir}/dahdi/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-%{pname}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-%{pname}
%depmod %{_kernel_ver}

%files devel
%{_includedir}/dahdi

%files -n kernel%{_alt_kernel}-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
