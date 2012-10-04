%if 0%{?el5}
%global pybasever 2.6
%global __python_ver 26
%global __python /usr/bin/python%{pybasever}
%global __os_install_post %{__multiple_python_os_install_post}
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           eucadw
Version:        3.2.0
Release:        0%{?build_id:.%build_id}%{?dist}
Summary:        CLI tools for the Eucalyptus Datawarehouse

Group:          Applications/System
License:        GPLv3 
URL:            http://www.eucalyptus.com
Source0:        %{name}-%{version}%{?tar_suffix}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
Requires:       eucadw-libs = %{version}-%{release}

%description
CLI tools for the Eucalyptus Datawarehouse

%package -n eucadw-libs
Summary:        Java libraries for %{name}
Group:          Applications/System
Requires:       java >= 1:1.6.0
Requires:       jpackage-utils

%description -n eucadw-libs
Java libraries for Eucalyptus Datawarehouse CLI tools

%prep
%setup -q -n eucadw-%{version}%{?tar_suffix}

%build
# Build CLI tools
pushd %{name}
%{__python} setup.py build
popd

# Build jar
ant

%install
rm -rf $RPM_BUILD_ROOT

# Install CLI tools
pushd %{name}
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/eucadw
install -pm 644 etc/eucadw.cfg $RPM_BUILD_ROOT/etc/eucadw/eucadw.cfg
popd

# Install jar
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}
install -pm 644 dist/eucalyptus-datawarehouse-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
install -pm 644 lib/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}

rm -f $RPM_BUILD_ROOT%{_javadir}/ant-*.jar

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/licenses
install -pm 644 /usr/share/eucalyptus/licenses/*.LICENSE $RPM_BUILD_ROOT%{_javadir}/%{name}/licenses

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}/*
/usr/bin/eucadw-*
%dir /etc/eucadw
%config /etc/eucadw/eucadw.cfg
%doc README.md LICENSE

%files -n eucadw-libs
%defattr(-,root,root,-)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%dir %{_javadir}/%{name}/licenses
%doc %{_javadir}/%{name}/licenses/*.LICENSE

%changelog
* Thu Oct 04 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.7
- Fixed license files being included twice

* Thu Sep 27 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.6
- Package renamed to eucadw
- Changed location of jars to /usr/share/java/eucadw

* Tue Sep 25 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.5
- Add BR of ant-linuxtools
- Add group field for bodega-libs subpackage

* Fri Sep 21 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.4
- Add licenses

* Thu Sep 20 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.3
- Now bundling java libraries in bodega-libs package

* Wed Sep 19 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.2
- Added java library

* Fri Aug 31 2012 Eucalyptus Release Engineering <support@eucalyptus.com> - 0-0.1
- Initial package build

