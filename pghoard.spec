%{?scl:%scl_package pghoard}
%{!?scl:%global pkg_name %{name}}

%global pypi_name pghoard

%define pybasever 3.3
%define pyver 33

%define upstream_name pghoard

%define name python%{pyver}-%{upstream_name}
%define __python /opt/rh/python33/root/usr/bin/python3


Name:           pghoard
Version:        %{major_version}
Release:        %{minor_version}%{?dist}
Url:            http://github.com/ohmu/pghoard
Summary:        PostgreSQL streaming backup service
License:        ASL 2.0
Source0:        pghoard-rpm-src.tar
Requires(pre):  shadow-utils
Requires:       postgresql92-server
Requires:       python33-python-boto, python33-python-cryptography python33-python-python-dateutil
Requires:       python33-python-psycopg2, python33-python-requests, python33-python-python-snappy
BuildRequires:  python33-python-devel
BuildArch:      noarch

%description
PGHoard is a PostgreSQL streaming backup service.  Backups are stored in
encrypted and compressed format in a cloud object storage.  PGHoard
currently supports Amazon Web Services S3, Google Cloud Storage, OpenStack
Swift and Ceph (using S3 or Swift interfaces with RadosGW.)
Support for Windows Azure is experimental.


%prep
%{?scl:scl enable %{scl} "}
%setup -q -n pghoard
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --root=%{buildroot}
sed -e "s@#!/bin/python@#!%{_bindir}/python@" -i %{buildroot}/opt/rh/python33/root/usr/bin/*
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/pghoard
%{?scl:"}
install -d %{buildroot}/etc/rc.d/init.d
install -m 755 pghoard.init %{buildroot}/etc/rc.d/init.d/pghoard


%check
# make test

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst pghoard.json
/opt/rh/python33/root/usr/bin/*
/opt/rh/python33/root/usr/lib/python3.3/site-packages/*
%attr(0755, postgres, postgres) %{_localstatedir}/lib/pghoard
/etc/rc.d/init.d/pghoard


%changelog
* Mon Dec 14 2015 Oskari Saarenmaa <os@ohmu.fi> - 0.9.0
- We're Python 3 only now

* Wed Mar 25 2015 Oskari Saarenmaa <os@ohmu.fi> - 0.9.0
- Build a single package using Python 3 if possible, Python 2 otherwise

* Thu Feb 26 2015 Oskari Saarenmaa <os@ohmu.fi> - 0.9.0
- Refactored

* Thu Feb 19 2015 Hannu Valtonen <hannu.valtonen@ohmu.fi> - 0.9.0
- Initial RPM package spec
