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

# Dependency of perl-Mail-DMARC

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)
%undefine _disable_source_fetch

Name:           perl-Net-IDN-Encode
Version:        2.500
Release:        1.eFa%{?dist}
Summary:        Internationalizing Domain Names in Applications (IDNA)
License:        perl_5
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Net::IDN::Encode
Source:         https://cpan.metacpan.org/authors/id/C/CF/CFAERBER/Net-IDN-Encode-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl-Unicode-Normalize

%description
This module provides an easy-to-use interface for encoding and decoding
Internationalized Domain Names (IDNs).

IDNs use characters drawn from a large repertoire (Unicode), but IDNA
allows the non-ASCII characters to be represented using only the ASCII
characters already allowed in so-called host names today
(letter-digit-hyphen, /[A-Z0-9-]/i).

Use this module if you just want to convert domain names (or email addresses),
using whatever IDNA standard is the best choice at the moment.

You should be familiar with Unicode support in perl, as this module expects
correctly encoded input. See perlunitut, perluniintro and perlunicode for
details.

%prep
%setup -q -n Net-IDN-Encode-%{version}

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes MANIFEST README LICENSE SIGNATURE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Mar 08 2023 Shawn Iverson <shawniverson@efa-project.org> - 2.500-1
- Built for eFa https://efa-project.org
