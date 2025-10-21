#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.0
%define		qtver		5.15.2
%define		kpname		libksysguard

Summary:	Library for monitoring your system
Name:		kp6-%{kpname}
Version:	6.5.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	fff58dbbe0ea61f5a974c48d6702c9ff
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Sensors-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcompletion-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	libnl-devel
BuildRequires:	libpcap-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRequires:	zlib-devel
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Library for monitoring your system.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < 6

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_datadir}/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
%{_datadir}/dbus-1/system-services/org.kde.ksysguard.processlisthelper.service
%{_datadir}/ksysguard
%{_datadir}/polkit-1/actions/org.kde.ksysguard.processlisthelper.policy
%{_datadir}/qlogging-categories6/libksysguard.categories
%ghost %{_libdir}/libprocesscore.so.10
%{_libdir}/libprocesscore.so.*.*
%ghost %{_libdir}/libKSysGuardFormatter.so.2
%{_libdir}/libKSysGuardFormatter.so.*.*
%ghost %{_libdir}/libKSysGuardSensorFaces.so.2
%{_libdir}/libKSysGuardSensorFaces.so.*.*
%ghost %{_libdir}/libKSysGuardSensors.so.2
%{_libdir}/libKSysGuardSensors.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/ksysguard
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/faces
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/formatter
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/process
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/sensors
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/ExtendedLegend.qml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/SensorFace.qml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/qmldir
%{_libdir}/qt6/qml/org/kde/ksysguard/formatter/qmldir
%{_libdir}/qt6/qml/org/kde/ksysguard/process/qmldir
%{_libdir}/qt6/qml/org/kde/ksysguard/sensors/qmldir
%{_datadir}/knsrcfiles/systemmonitor-faces.knsrc
%{_datadir}/knsrcfiles/systemmonitor-presets.knsrc
%ghost %{_libdir}/libKSysGuardSystemStats.so.2
%{_libdir}/libKSysGuardSystemStats.so.*.*.*
%dir %{_libdir}/qt6/plugins/ksysguard
%dir %{_libdir}/qt6/plugins/ksysguard/process
%{_libdir}/qt6/plugins/ksysguard/process/ksysguard_plugin_gpu.so
%{_libdir}/qt6/plugins/ksysguard/process/ksysguard_plugin_network.so
%dir %{_prefix}/libexec/ksysguard
%attr(755,root,root) %{_prefix}/libexec/ksysguard/ksgrd_network_helper
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/SensorRangeSpinBox.qml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/Choices.qml
%{_libdir}/qt6/plugins/kf6/packagestructure/ksysguard_sensorface.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/ksysguardprocesslist_helper
%{_datadir}/dbus-1/interfaces/org.kde.ksystemstats1.xml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/CompactSensorFace.qml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/SensorFaces.qmltypes
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/SuffixSpinBox.qml
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/libSensorFacesplugin.so
%dir %{_libdir}/qt6/qml/org/kde/ksysguard/faces/private
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/private/SensorFacesPrivate.qmltypes
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/private/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/private/libSensorFacesPrivate.so
%{_libdir}/qt6/qml/org/kde/ksysguard/faces/private/qmldir
%{_libdir}/qt6/qml/org/kde/ksysguard/formatter/Formatter.qmltypes
%{_libdir}/qt6/qml/org/kde/ksysguard/formatter/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/ksysguard/formatter/libFormatterplugin.so
%{_libdir}/qt6/qml/org/kde/ksysguard/process/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/ksysguard/sensors/Sensors.qmltypes
%{_libdir}/qt6/qml/org/kde/ksysguard/process/libprocesscoreplugin.so
%{_libdir}/qt6/qml/org/kde/ksysguard/process/processcore.qmltypes
%{_libdir}/qt6/qml/org/kde/ksysguard/sensors/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/ksysguard/sensors/libSensorsplugin.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/ksysguard
%{_libdir}/cmake/KSysGuard
%{_libdir}/libKSysGuardFormatter.so
%{_libdir}/libKSysGuardSensorFaces.so
%{_libdir}/libKSysGuardSensors.so
%{_libdir}/libKSysGuardSystemStats.so
%{_libdir}/libprocesscore.so
