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

Name:           perl-Test-File-ShareDir
Version:        1.001002
Release:        1.eFa%{?dist}
Summary:        Create a Fake ShareDir for your modules for testing.
License:        perl_5
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Test::File::ShareDir
Source:         https://cpan.metacpan.org/authors/id/K/KE/KENTNL/Test-File-ShareDir-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: perl-Carp
Requires: perl-Class-Tiny
Requires: perl-Exporter
Requires: perl-File-Copy-Recursive
Requires: perl-File-ShareDir >= 1.00
Requires: perl-Path-Tiny
Requires: perl-Scope-Guard
Requires: perl-parent
Requires: perl(strict)
Requires: perl(warnings)

%description
Test::File::ShareDir is some low level plumbing to enable a distribution to
perform tests while consuming its own share directories in a manner similar
to how they will be once installed.

This allows File::ShareDir to see the latest version of content instead of
simply whatever is installed on whichever target system you happen to be
testing on.

Note: This module only has support for creating 'new' style share dirs and
are NOT compatible with old File::ShareDirs.

For this reason, unless you have File::ShareDir 1.00 or later installed, this
module will not be usable by you.

%prep
%setup -q -n Test-File-ShareDir-%{version}

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
%doc Changes MANIFEST README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Mar 08 2023 Shawn Iverson <shawniverson@efa-project.org> - 1.001002-1
- Built for eFa https://efa-project.org
