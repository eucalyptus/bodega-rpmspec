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
BuildRequires:  python%{?__python_ver}-devel

Requires:       eucalyptus-common-java-libs

%description
CLI tools for the Eucalyptus Datawarehouse

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

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
/usr/bin/eucadw-import-data
/usr/bin/eucadw-generate-report
/usr/share/eucalyptus/bodega.jar
%dir /etc/eucadw
%config /etc/eucadw/eucadw.cfg

%changelog
* Wed Sep 19 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.2
- Added java library

* Fri Aug 31 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.1
- Initial package build

