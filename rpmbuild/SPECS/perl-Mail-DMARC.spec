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

Name:           perl-Mail-DMARC
Version:        1.20230215
Release:        1.eFa%{?dist}
Summary:        Perl implementation of DMARC
License:        perl_5
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Mail::DMARC
Source0:        https://cpan.metacpan.org/authors/id/M/MB/MBRADSHAW/Mail-DMARC-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl-File-ShareDir-Install
BuildRequires:  perl-File-ShareDir
BuildRequires:  perl-Test-Output
BuildRequires:  perl-Config-Tiny
BuildRequires:  perl-DBD-SQLite >= 1.31
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-XML-LibXML
BuildRequires:  perl-Email-MIME
BuildRequires:  perl-Net-DNS
BuildRequires:  perl-Net-IP
BuildRequires:  perl-Regexp-Common >= 2013031301
BuildRequires:  perl-Socket6 >= 0.23
BuildRequires:  perl-DBIx-Simple >= 1.35
BuildRequires:  perl-Email-Sender 
BuildRequires:  perl-Email-Simple
BuildRequires:  perl-Test-File-ShareDir
BuildRequires:  perl-Net-IDN-Encode
Requires: perl-Carp
Requires: perl-Config-Tiny
Requires: perl-DBD-SQLite >= 1.31
Requires: perl-DBIx-Simple
Requires: perl-Data-Dumper
Requires: perl-Email-MIME
Requires: perl-Email-Sender 
Requires: perl-Email-Simple
Requires: perl-Encode
Requires: perl-English
Requires: perl-File-ShareDir
Requires: perl-Getopt-Long
Requires: perl-HTTP-Tiny
Requires: perl-IO-Compress
Requires: perl-IO
Requires: perl-IO-Socket-SSL
Requires: perl(IO::Uncompress::Gunzip)
Requires: perl(IO::Uncompress::Unzip)
Requires: perl-Net-DNS
Requires: perl-Net-IDN-Encode
Requires: perl-Net-IP
Requires: perl-Net-SSLeay
Requires: perl-POSIX
Requires: perl-Pod-Usage
Requires: perl-Regexp-Common >= 2013031301
Requires: perl-Socket
Requires: perl-Socket6 >= 0.23
Requires: perl-Sys-Hostname
Requires: perl-Sys-Syslog
Requires: perl-Test-File-ShareDir
Requires: perl-URI
Requires: perl-XML-LibXML

%description
This module is a suite of tools for implementing DMARC. It adheres to the 
2013 DMARC draft, intending to implement every MUST and every SHOULD.

This module can be used by...

    MTAs and filtering tools like SpamAssassin to validate that incoming
    messages are aligned with the purported sender's policy.

    email senders, to receive DMARC reports from other mail servers and
    display them via CLI and web interfaces.

    MTA operators to send DMARC reports to DMARC author domains.

%prep
%setup -q -n Mail-DMARC-%{version}

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
%doc Changes.md MANIFEST LICENSE README.md
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Mon Mar 6 2023 Shawn Iverson <shawniverson@efa-project.org> - 1.20230215-1
- Built for eFa https://efa-project.org
