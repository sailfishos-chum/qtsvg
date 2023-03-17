%global qt_version 5.15.8

Summary: Qt5 - Support for rendering and displaying SVG
Name: opt-qt5-qtsvg
Version: 5.15.8
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: pkgconfig(zlib)

BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}

%description
Scalable Vector Graphics (SVG) is an XML-based language for describing
two-dimensional vector graphics. Qt provides classes for rendering and
displaying SVG drawings in widgets and on other paint devices.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%ldconfig_scriptlets

%files
%license LICENSE.*
%{_opt_qt5_libdir}/libQt5Svg.so.5*
%{_opt_qt5_plugindir}/iconengines/libqsvgicon.so
%{_opt_qt5_plugindir}/imageformats/libqsvg.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QSvg*Plugin.cmake

%files devel
%{_opt_qt5_headerdir}/QtSvg/
%{_opt_qt5_libdir}/libQt5Svg.so
%{_opt_qt5_libdir}/libQt5Svg.prl
%dir %{_opt_qt5_libdir}/cmake/Qt5Svg/
%{_opt_qt5_libdir}/cmake/Qt5Svg/Qt5SvgConfig*.cmake
%{_opt_qt5_libdir}/pkgconfig/Qt5Svg.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_svg*.pri

%files examples
%{_opt_qt5_examplesdir}/
