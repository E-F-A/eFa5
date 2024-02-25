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

%undefine _disable_source_fetch

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define		pdir	Net
%define		pnam	LibIDN
Summary:	This module provides Perl bindings for GNU Libidn
Name:		perl-Net-LibIDN
Version:	0.12
Release:	1.eFa%{?dist}
License:	GPL
Group:		Development/Languages/Perl
Source0:	https://cpan.metacpan.org/authors/id/T/TH/THOR/%{pdir}-%{pnam}-%{version}.tar.gz
URL:		https://metacpan.org/pod/Net::LibIDN
BuildRequires:	libidn-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRoot:	    %{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Patch0:	Net-LibIDN-0.12.patch

%description
This module provides Perl bindings for GNU Libidn by Simon Josefsson
(http://www.gnu.org/software/libidn/)

# %description -l pl.UTF-8
# TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p2

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

find %{buildroot} -name .packlist -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/Net/*.pm
%dir %{perl_vendorarch}/auto/Net/LibIDN
%{perl_vendorarch}/auto/Net/LibIDN/*.ix
%attr(755,root,root) %{perl_vendorarch}/auto/Net/LibIDN/*.so
%{_mandir}/man3/*.3pm*

%changelog
* Mon Mar 6 2023 Shawn Iverson <shawniverson@efa-project.org> 0.12-1
- Updated for eFa https://efa-project.org