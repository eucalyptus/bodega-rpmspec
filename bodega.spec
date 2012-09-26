%if 0%{?el5}
%global pybasever 2.6
%global __python_ver 26
%global __python /usr/bin/python%{pybasever}
%global __os_install_post %{__multiple_python_os_install_post}
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           python%{?__python_ver}-bodega
Version:        0
Release:        0%{?build_id:.%build_id}%{?dist}
Summary:        Client user interface for Eucalyptus

Group:          Applications/System
License:        GPLv3 
URL:            http://www.eucalyptus.com
Source0:        bodega-%{version}%{?tar_suffix}.tar.gz
BuildRoot:      %{_tmppath}/bodega-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  eucalyptus-common-java-libs
BuildRequires:  ant-linuxtools
BuildRequires:  python%{?__python_ver}-devel
BuildRequires:  python%{?__python_ver}-setuptools
BuildRequires:  ant >= 1.7.0
BuildRequires:  apache-ivy
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils

Requires:       python%{?__python_ver}
Requires:       bodega-libs = %{version}-%{release}

%description
CLI tools for the Eucalyptus Datawarehouse

%package -n bodega-libs
Summary:        CLI tools for the Eucalyptus Datawarehouse
Requires:       java >= 1:1.6.0
Requires:       jpackage-utils
Conflicts:      eucalyptus-common-java-libs

%description -n bodega-libs
Java libraries for Eucalyptus Datawarehouse CLI tools

%prep
%setup -q -n bodega-%{version}%{?tar_suffix}

%build
# Build CLI tools
pushd eucadw
%{__python} setup.py build
popd

# Build bodega.jar
ant


%install
rm -rf $RPM_BUILD_ROOT

# Install CLI tools
pushd eucadw
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/eucadw
install -pm 644 etc/eucadw.cfg $RPM_BUILD_ROOT/etc/eucadw/eucadw.cfg
popd

# Install bodega.jar
install -d $RPM_BUILD_ROOT/usr/share/eucalyptus
install -pm 644 dist/bodega.jar $RPM_BUILD_ROOT/usr/share/eucalyptus
install -pm 644 lib/*.jar $RPM_BUILD_ROOT/usr/share/eucalyptus

rm -f $RPM_BUILD_ROOT/usr/share/eucalyptus/ant-*.jar

install -d $RPM_BUILD_ROOT/usr/share/eucalyptus/licenses
install -pm 644 /usr/share/eucalyptus/licenses/*.LICENSE $RPM_BUILD_ROOT/usr/share/eucalyptus/licenses

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
/usr/bin/eucadw-import-data
/usr/bin/eucadw-generate-report
%dir /etc/eucadw
%config /etc/eucadw/eucadw.cfg
%doc README.md LICENSE

%files -n bodega-libs
%defattr(-,root,root,-)
%dir /usr/share/eucalyptus
/usr/share/eucalyptus/*.jar
%dir /usr/share/eucalyptus/licenses
%doc /usr/share/eucalyptus/licenses/*.LICENSE

%changelog
* Fri Sep 21 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.4
- Add licenses

* Thu Sep 20 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.3
- Now bundling java libraries in bodega-libs package

* Wed Sep 19 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.2
- Added java library

* Fri Aug 31 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.1
- Initial package build

