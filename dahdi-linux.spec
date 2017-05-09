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
%bcond_without  kernel		# don't build kernel modules
%bcond_with	oslec		# with Open Source Line Echo Canceller
%bcond_without	xpp		# without Astribank
%bcond_without	userspace	# don't build userspace packages
%bcond_with	verbose

%ifarch alpha
%undefine	with_xpp
%endif

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel	0.1
%define		pname	dahdi-linux
%define		FIRMWARE_URL http://downloads.digium.com/pub/telephony/firmware/releases
Summary:	DAHDI telephony device support
Summary(pl.UTF-8):	Obsługa urządzeń telefonicznych DAHDI
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	2.11.1
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://downloads.asterisk.org/pub/telephony/dahdi-linux/releases/dahdi-linux-%{version}.tar.gz
# Source0-md5:	af96917e15eebc36519948133ec7e36b
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
URL:		http://www.asterisk.org/
%{?with_kernel:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}}
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Rules:
# - modules_X: single modules, just name module with no suffix
# - modules_X: subdir modules are just directory name with slash like dirname/
# - keep X and X_in in sync
# - X is used for actual building (entries separated with space), X_in for pld macros (entries separated with comma)

%define	modules_1	dahdi.o dahdi_dynamic.o dahdi_dynamic_eth.o dahdi_dynamic_ethmf.o dahdi_dynamic_loc.o dahdi_echocan_jpah.o dahdi_echocan_kb1.o dahdi_echocan_mg2.o dahdi_echocan_sec.o dahdi_echocan_sec2.o pciradio.o tor2.o wcfxo.o wct1xxp.o wctdm.o wcte11xp.o
%define	modules_1_in	dahdi,dahdi_dynamic,dahdi_dynamic_eth,dahdi_dynamic_ethmf,dahdi_dynamic_loc,dahdi_echocan_jpah,dahdi_echocan_kb1,dahdi_echocan_mg2,dahdi_echocan_sec,dahdi_echocan_sec2,pciradio,tor2,wcfxo,wct1xxp,wctdm,wcte11xp
%define	modules_2	voicebus/ wct4xxp/ wcte12xp/ %{?with_xpp:xpp/}
%define	modules_2_in	voicebus/dahdi_voicebus,wct4xxp/wct4xxp,wcte12xp/wcte12xp,%{?with_xpp:xpp/xpd_bri,xpp/xpd_echo,xpp/xpd_fxo,xpp/xpd_fxs,xpp/xpd_pri,xpp/xpp,xpp/xpp_usb}
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
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu dahdi
Group:		Development/Libraries

%description devel
Header files for dahdi interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe interfejsu dahdi.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-%{pname}\
Summary:	DAHDI Linux kernel driver\
Summary(pl.UTF-8):	Sterownik DAHDI dla jądra Linuksa\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%{?with_oslec:Requires:	kernel-misc-oslec = 20070608-0.1@%{_kernel_ver_str}}\
\
%description -n kernel%{_alt_kernel}-%{pname}\
DAHDI telephony Linux kernel driver.\
\
%description -n kernel%{_alt_kernel}-%{pname} -l pl.UTF-8\
Sterownik dla jądra Linuksa do urządzeń telefonicznych DAHDI.\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-%{pname}\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/dahdi*.ko*\
/lib/modules/%{_kernel_ver}/misc/pciradio.ko*\
/lib/modules/%{_kernel_ver}/misc/tor2.ko*\
/lib/modules/%{_kernel_ver}/misc/wcb4xxp.ko*\
/lib/modules/%{_kernel_ver}/misc/wcfxo.ko*\
/lib/modules/%{_kernel_ver}/misc/wct1xxp.ko*\
/lib/modules/%{_kernel_ver}/misc/wct4xxp.ko*\
/lib/modules/%{_kernel_ver}/misc/wctc4xxp.ko*\
/lib/modules/%{_kernel_ver}/misc/wctdm.ko*\
/lib/modules/%{_kernel_ver}/misc/wctdm24xxp.ko*\
/lib/modules/%{_kernel_ver}/misc/wcte11xp.ko*\
/lib/modules/%{_kernel_ver}/misc/wcte12xp.ko*\
%if %{with xpp}\
/lib/modules/%{_kernel_ver}/misc/xpd_*.ko*\
/lib/modules/%{_kernel_ver}/misc/xpp.ko*\
/lib/modules/%{_kernel_ver}/misc/xpp_usb.ko*\
%endif\
%endif\
\
%post -n kernel%{_alt_kernel}-%{pname}\
%depmod %{_kernel_ver}\
\
%postun -n kernel%{_alt_kernel}-%{pname}\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%if %{with kernel}\
%build_kernel_modules SUBDIRS=$PWD/drivers/dahdi DAHDI_BUILD_ALL=m HOTPLUG_FIRMWARE=yes DAHDI_MODULES_EXTRA=" " -m %{modules_in} KSRC=$PWD/o -C drivers/dahdi DAHDI_INCLUDE=$PWD/../../include\
cd drivers/dahdi\
%install_kernel_modules -D ../../installed -m %{modules_in} -d misc\
cd ../..\
%endif\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q -n %{pname}-%{version}

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

%{?with_kernel:%{expand:%build_kernel_packages}}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/dahdi

%if %{with userspace}
%{__make} install-include \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with kernel}
cp -a installed/* $RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%files devel
%defattr(644,root,root,755)
%{_includedir}/dahdi
%endif
