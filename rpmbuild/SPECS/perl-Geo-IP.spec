#-----------------------------------------------------------------------------#
# eFa SPEC file definition
#-----------------------------------------------------------------------------#
# Copyright (C) 2023 https://efa-project.org
#
# This SPEC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This SPEC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this SPEC. If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------#

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)
%undefine _disable_source_fetch

Name:           perl-Geo-IP
Version:        1.51
Release:        1.eFa%{?dist}
Summary:        Look up location and network information by IP Address
License:        perl_5
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Geo::IP
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MAXMIND/Geo-IP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 1.302183
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl-DynaLoader
Requires:       perl-Exporter
Requires:       perl-base
Requires:       perl(strict)
Requires:       perl-vars

%description
This module uses the GeoIP Legacy file based database. This database simply
contains IP blocks as keys, and countries as values. This database should be
more complete and accurate than reverse DNS lookups.

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

%prep
%setup -q -n Geo-IP-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;
find %{buildroot} -name perllocal.pod -exec %{__rm} {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

# Remove man conflict with perl package
#%{__rm} -rf %{buildroot}/%{_mandir}/man3

%{_fixperms} %{buildroot}/*

%check
%{__make} test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes MANIFEST LICENSE README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*.3pm*

%changelog
* Mon Mar 6 2023 Shawn Iverson <shawniverson@efa-project.org> - 1.51-1
- Built for eFa https://efa-project.org
