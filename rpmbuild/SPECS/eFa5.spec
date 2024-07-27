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

%define releasenum 11

Name:      eFa
Summary:   eFa Maintenance rpm
Version:   5.0.0
Release:   %{releasenum}.eFa%{?dist}
Group:     Applications/System
URL:       https://efa-project.org
License:   GNU GPL v3+
Source0:   eFa-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# Control dependencies here as updates are released
# Use version and release numbers required for each update
# to maintain strict version control and dependency resolution
Requires:  clamav >= 0.103.8-3
    # clamav                                     # epel    # AV
Requires:  clamav-update >= 0.103.8-3
    # clamav-update                              # epel    # AV
Requires:  clamd >= 0.103.8-3
    # clamd			                             # epel    # AV
Requires:  mariadb-server >= 3:10.5.16-2
    # mariadb-server                             # base    # postfix, mailwatch
Requires:  php >= 8.0.27-1
    # php                                        # base    # mailwatch, frontend
Requires:  php-gd >= 8.0.27-1
    # php-gd                                     # base    # mailwatch, frontend
Requires:  php-mysqlnd >= 8.0.27-1
    # php-mysqlnd                                # base    # mailwatch, frontend
Requires:  php-ldap >= 8.0.27-1
    # php-ldap                                   # base    # mailwatch, frontend
Requires:  php-mbstring >= 8.0.27-1
    # php-mbstring                               # base    # mailwatch, frontend
Requires:  httpd >= 2.4.53-7
    # httpd                                      # base    # mailwatch, frontend
Requires:  cyrus-sasl-md5 >= 2.1.27-20
    # cyrus-sasl-md5                             # base    # postfix
Requires:  mod_ssl >= 1:2.4.53-7
    # mod_ssl                                    # base    # httpd
Requires:  postfix >= 2:3.5.23-1
    # postfix                                    # eFa     # MTA
Requires:  unbound >= 1.16.2-2
    # unbound                                    # eFa     # DNS
Requires:  dnf-automatic >= 4.12.0-4
    # dnf auto updates                           # base    # dnf-automatic
Requires:  checkpolicy >= 3.4-1
    # checkpolicy                                # base    # selinux
Requires: php-fpm >= 8.0.27-1
    # php-fpm                                    # base    # mailwatch, frontend
Requires: php-process >= 8.0.27-1
    # php-process                                # base    # eFaInit
Requires: php-json >= 8.0.27-1
    # php-json                                   # base    # eFaInit
Requires: php-cli >= 8.0.27-1
    # php-cli                                    # base    # mailwatch, frontend
Requires: php-xml >= 8.0.27-1
    # php-xml                                    # base    # mailwatch, frontend
Requires: dovecot >= 1:2.3.16-7
    # dovecot                                    # base    # postfix
Requires: virt-what >= 1.25-1
    # virt-what                                  # base    # eFa
Requires: openssh-server >= 8.7p1-24
    # openssh-server                             # base    # eFa
Requires: sudo >= 1.9.5p2-7
    # sudo                                       # base    # eFa
Requires: chrony >= 4.2-1
    # chrony                                     # base    # eFa
Requires: firewalld >= 1.1.1-3
    # firewalld                                  # base    # eFa
Requires: python3-certbot-apache >= 2.1.0-1
    #                                            # epel    # mailwatch, frontend
Requires: rsync => 3.2.3-18
    #                                            # base    # clamd
Requires: opendkim >= 2.11.0-0.28
    #                                            # epel    # eFa
Requires: cyrus-sasl >= 2.1.27-20
    #                                            # base    # eFa
Requires: cyrus-sasl-lib >= 2.1.27-20
    #                                            # base    # eFa
Requires: cyrus-sasl-plain >= 2.1.27-20
    #                                            # base    # eFa
Requires: opendmarc >= 1.4.2-10
    #                                            # epel    # eFa
Requires: perl-Switch >= 2.17-23
    #                                            # base    # opendmarc
Requires: fail2ban >= 1.0.1-2
    #                                            # epel    # eFa
Requires: rsyslog >= 8.2102.0-105
    #                                            # base    # eFa
Requires: NetworkManager >= 1.42.2-1
    #                                            # base    # eFa
Requires: php-gmp >=  8.0.27-1
    #                                            # appstream # eFa
Requires: ipcalc >= 1.0.0-5
    #                                            # base    # eFa
Requires: perl >= 4:5.32.1-479
    #                                            # appstream # MailScanner
Requires: perl-Archive-Zip >= 1.68-6
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Carp >= 1.50-460
    #                                            # appstream # MailScanner
Requires: perl-Compress-Raw-Zlib >= 2.101-5
    #                                            # appstream # MailScanner
Requires: perl-IO-Compress >= 2.102-4
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Data-Dumper >= 2.174-462
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-DateTime >= 2:1.54-4
    #                                            # crb       # MailScanner
Requires: perl-DBI >= 1.643-9
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Digest-MD5 >= 2.58-4
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-DirHandle >= 1.05-479
    #                                            # appstream # MailScanner
Requires: perl-Encode >= 4:3.08-462
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Env >= 1.04-460
    #                                            # appstream # MailScanner
Requires: perl-Fcntl >= 1.13-479
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-File-Basename >= 2.85-479
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-File-Copy >= 2.34-479
    #                                            # appstream # MailScanner
Requires: perl-FileHandle >= 2.03-479
    #                                            # appstream # MailScanner
Requires: perl-File-Path >= 2.18-4
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Filesys-Df >= 0.92-45
    #                                            # epel      # MailScanner
Requires: perl-File-Temp >= 1:0.231.100-4
    #                                            # appstream # MailScanner
Requires: perl-Getopt-Long >= 1:2.52-4
    #                                            # appstream # MailScanner
Requires: perl-HTML-Parser >= 3.76-3
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-IO-stringy >= 2.113-7
    #                                            # crb       # MailScanner
Requires: perl-libwww-perl >= 6.53-4
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-MIME-tools >= 5.509-11
    #                                            # epel      # MailScanner
Requires: perl-Net-CIDR >= 0.21-1
    #                                            # epel      # MailScanner
Requires: perl-Net-DNS >= 1.29-4
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-OLE-Storage_Lite >= 0.20-7
    #                                            # epel      # MailScanner
Requires: perl-POSIX >= 1.94-479
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Socket >= 4:2.031-4
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Sys-Syslog >= 0.36-461
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Time-HiRes >= 4:1.9764-462
    #                                            # appstream # MailScanner, spamassassin
Requires: perl-Time-Local >= 2:1.300-7
    #                                            # appstream # MailScanner, spamassassin
Requires: MailScanner >= 5.5.1-5
    # MailScanner                                # eFa     # MailScanner
Requires: p7zip >= 16.02-21
    # p7zip                                      # epel    # MailScanner
Requires: p7zip-plugins >= 16.02-21
    # p7zip-plugins                              # epel    # MailScanner
Requires: file >= 5.39-10
    # file                                       # base    # MailScanner
Requires: tar >= 2:1.34-6
    #                                            # base    # MailScanner
Requires: perl-Net-DNS-Resolver-Programmable >= 0.009-1
    #                                            # eFa     # MailScanner
Requires: perl-Sendmail-PMilter >= 1.24-1
    #                                            # eFa     # MailScanner
Requires: perl-Sys-Hostname-Long >= 1.5-1
    #                                            # eFa     # MailScanner
Requires: perl-Sys-SigAction >= 0.23-1
    #                                            # eFa     # MailScanner
Requires: tnef >= 1.4.18-1
    #                                            # eFa     # MailScanner
Requires: unrar >= 6.2.5-1
    #                                            # eFa     # MailScanner
Requires:  pyzor >= 1.0.0-28.20200530gitf46159b
    # pyzor                                      # epel    # spamassassin
Requires:  re2c >= 2.2-1
    # re2c                                       # epel    # spamassassin
Requires:  dcc >= 2.3.168-1
    # dcc                                        # eFa     # spamassassin
Requires:  perl-Archive-Tar >= 2.38-6
    # perl-Archive-Tar                           # appstream # spamassassin
Requires:  perl-Archive-Tar >= 2.38-6
    # perl-Carp                                  # appstream # spamassassin
Requires:  perl-Digest-SHA >= 1:6.02-461
    # perl-Digest-SHA                            # appstream # spamassassin
Requires:  perl-Errno >= 1.30-479
    #                                            # appstream # spamassassin
Requires:  perl-Exporter >= 5.74-461
    #                                            # appstream # spamassassin
Requires:  perl-IO-Zlib >= 1:1.11-4
    #                                            # appstream # spamassassin
Requires:  perl-NetAddr-IP >= 4.079-18
    #                                            # appstream # spamassassin
Requires:  perl-Storable >= 1:3.21-460
    #                                            # appstream # spamassassin
Requires:  perl-version >= 7:0.99.28-4
    #                                            # appstream # spamassassin
Requires:  perl-BSD-Resource >= 1.291.100-17
    #                                            # appstream # spamassassin
Requires:  perl-DB_File >= 1.855-4
    #                                            # appstream # spamassassin
Requires:  perl-DBD-SQLite >= 1.66-5
    # perl-DBD-SQLite                            # appstream # spamassassin
Requires:  perl-Digest-SHA1 >= 2.13-34
    # perl-Digest-SHA1                           # appstream # spamassassin
Requires: perl-Email-Address-XS >= 1.04-13
    #                                            # appstream # spamassassin
Requires: perl-IO-Socket-INET6 >= 2.72-24
    #                                            # appstream # spamassassin
Requires: perl-IO-Socket-IP >= 0.41-5
    #                                            # appstream # spamassassin
Requires: perl-IO-Socket-SSL >= 2.073-1
    #                                            # appstream # spamassassin
Requires: perl-IO-String >= 1.08-43
    # perl-IO-String                             # crb       # spamassassin
Requires: perl-Mail-DKIM >= 1.20200907-4
    #                                            # appstream # spamassassin
Requires: perl-Mail-SPF >= 2.9.0-26
    #                                            # appstream # spamassassin
Requires: perl-MaxMind-DB-Reader >= 1.000014-9
    #                                            # epel      # spamassassin
Requires: perl-MaxMind-DB-Reader-XS >= 1.000009-3
    #                                            # epel      # spamassassin
Requires: perl-MIME-Base64 >= 3.16-4
    #                                            # appstream # spamassassin
Requires: perl-Net-CIDR-Lite >= 0.22-2
    #                                            # appstream # spamassassin
Requires: perl-Net-DNS-Nameserver >= 1.29-6
    #                                            # crb       # spamassassin
Requires: perl-Net-LibIDN2 >= 1.01-7
    #                                            # epel      # spamassassin
Requires: perl-Net-Patricia >= 1.22-25
    #                                            # epel      # spamassassin
Requires:  perl-Razor-Agent >= 2.86-1
    # perl-Razor-Agent                           # epel      # spamassassin
Requires: perl-IP-Country-DB_File >= 3.03-1
    #                                            # eFa       # spamassassin
Requires: perl-Net-LibIDN >= 0.12-1
    #                                            # eFa       # spamassassin
Requires: perl-Encode-Detect >= 1.01-37
    #                                            # appstream # spamassassin
Requires: perl-Geo-IP >= 1.51-1
    #                                            # eFa       # spamassassin
Requires: perl-IP-Country >= 2.28-1
    #                                            # eFa       # spamassassin
Requires: perl-Mail-DMARC >= 1.20230215-1
    #                                            # eFa       # spamassassin
Requires:  perl-Encoding-FixLatin >= 1.04-1
    # perl-Encoding-FixLatin                     # eFa       # MailWatch
Requires:  tmpwatch >= 2.11-20
    # tmpwatch                                   # appstream # Spamassassin
Requires:  sqlgrey >= 1:1.8.0-8
    # sqlgrey                                    # eFa       # Greylisting
Requires: sqlgreywebinterface >= 1:1.1.9-5
    # sqlgreywebinterrface                       # eFa       # mailwatch
Requires:  MailWatch >= 1:1.2.23-4
    # MailWatch                                  # eFa     # MailWatch Frontend
Requires:  spamassassin >= 4.0.1-2
    # spamassassin                               # eFa     # MailScanner
Requires:  clamav-unofficial-sigs >= 1:7.2.5.1-1
    # clamav-unofficial-sigs                     # eFa     # clamav
Requires: eFa-base >= 5.0.0-1
    # eFa-base                                   # eFa     # eFa
Requires:  perl-DBD-MySQL >= 4.050-13
    # perl-DBD-mysql                             # base    # spamassassin
Requires: chkconfig >= 1.20-2
    #                                            # base    # dcc
Requires: perl-LWP-Protocol-https >= 6.10-4
    #                                            # appstream # spamassassin
Requires: perl-Devel-Cycle >= 1.12-16
    #                                            # epel    # spamassassin
Requires: certbot >= 2.9.0-1
    #                                            # epel    # eFa
Requires: tuned >= 2.22.1-1
    #                                            # base    # eFa
Requires: bash-completion >= 1:2.11-5
    #                                            # base    # eFa
Requires: vim-enhanced >= 8.2.2637-20
    #                                            # base    # eFa

# Unverified dependencies
#Requires:  openssl-devel >= 1:3.0.7-5
#    # openssl-devel                              # base    # MailScanner
#Requires:  patch >= 2.7.6-16
#    # patch                                      # base    # MailScanner
#Requires:  bzip2-devel >= 1.0.6-13
#    # bzip2-devel                                # base    # MailScanner
#Requires:  gcc >= 4.8.5-36
#    # gcc                                        # base    # MailScanner
#Requires:  perl-Convert-BinHex >= 1.119-20
#    # perl-Convert-BinHex                        # epel    # MailScanner
#Requires:  perl-Convert-TNEF >= 0.18-2
#    # perl-Convert-TNEF                          # epel    # MailScanner
#Requires:  perl-CPAN >= 1.9800-293
#    # perl-CPAN                                  # base    # MailScanner
#Requires:  perl-Data-Dump >= 1.22-1
#    # perl-Data-Dump                             # epel    # MailScanner
#Requires:  perl-Digest-HMAC >= 1.03-5
#    # perl-Digest-HMAC                           # base    # MailScanner
#Requires:  perl-Encode-Detect >= 1.01-13
#    # perl-Encode-Detect                         # base    # MailScanner
#Requires:  perl-ExtUtils-CBuilder >= 0.28.2.6-293
#    # perl-ExtUtils-CBuilder                     # base    # MailScanner
#Requires:  perl-ExtUtils-MakeMaker >= 6.68-3
#    # perl-ExtUtils-MakeMaker                    # base    # MailScanner
#Requires:  perl-File-ShareDir-Install >= 0.08-1
#    # perl-File-ShareDir-Install                 # epel    # MailScanner
#Requires:  perl-Inline >= 0.53-4
#    # perl-Inline                                # base    # MailScanner
#Requires:  perl-LDAP >= 0.56-6
#    # perl-LDAP                                  # base    # MailScanner
#Requires:  perl-Mail-IMAPClient >= 3.37-1
#    # perl-Mail-IMAPClient                       # epel    # MailScanner
#Requires:  perl-Module-Build >= 0.40.05-2
#    # perl-Module-Build                          # base    # MailScanner
#Requires:  perl-Net-IP >= 1.26-4
#    # perl-Net-IP                                # epel    # MailScanner
#Requires:  perl-Test-Manifest >= 1.23-2
#    # perl-Test-Manifest                         # base    # MailScanner
#Requires:  perl-Test-Pod >= 1.48-3
#    # perl-Test-Pod                              # base    # MailScanner
#Requires:  perl-YAML >= 0.84-5
#    # perl-YAML                                  # base    # MailScanner
#Requires:  libtool-ltdl >= 2.4.2-22
#    # libtool-ltdl                               # base    # MailScanner
#Requires:  perl-IP-Country >= 2.28-1
#    # perl-IP-Country                            # eFa     # MailScanner, Spamassassin
#Requires:  perl-Mail-SPF-Query >= 1.999.1-1
#    # perl-Mail-SPF-Query                        # eFa     # MailScanner
#Requires:  perl-Geography-Countries >= 2009041301-17
#    # perl-Geography-Countries                   # eFa     # Spamassassin
#Requires:  perl-libnet >= 3.11-1
#    # perl-libnet                                # eFa     # Spamassassin
#Requires: perl-Math-Int64 >= 0.52
#    #                                            # epel    # spamassassin
#Requires: perl-namespace-autoclean >= 0.19-1
#    #                                            # epel    # spamassassin
#Requires: perl-Data-IEEE754 >= 0.02-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Data-Printer >= 0.40-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Data-Validate-IP >= 0.27-1
#    #                                            # eFa     # spamassassin
#Requires: perl-GeoIP2-Country-Reader >= 2.006002-1
#    #                                            # eFa     # spamassassin
#Requires: perl-List-AllUtils >= 0.15-1
#    #                                            # eFa     # spamassassin
#Requires: perl-List-SomeUtils >= 0.58-1
#    #                                            # eFa     # spamassassin
#Requires: perl-List-UtilsBy >= 0.11-1
#    #                                            # eFa     # spamassassin
#Requires: perl-MaxMind-DB-Metadata >= 0.040001-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Module-Runtime >= 0.016-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Moo >= 2.003006-1
#    #                                            # eFa     # spamassassin
#Requires: perl-MooX-StrictConstructor >= 0.010-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Role-Tiny >= 2.001004-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Scalar-List-Utils >= 1.53-1
#    #                                            # eFa     # spamassassin
#Requires: perl-strictures >= 2.000006-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Sub-Quote >= 2.006006-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Math-Int128 >= 0.22-1
#    #                                            # eFa     # spamassassin
#Requires: perl-Net-Works-Network >= 0.22-1
#    #                                            # eFa     # spamassassin


%description
eFa stands for Email Filter Appliance. eFa is born out of a need for a
cost-effective email virus & spam scanning solution after the ESVA project
died.

We try to create a complete package using existing open-source anti-spam
projects and combine them to a single easy to use (virtual) appliance.

For more information go to https://efa-project.org

eFa v5 is a rebuild of the previous eFa v4; the same components are used whenever
possible but are all updated to the latest version.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

# Move eFa-Configure into position
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/eFa-Configure
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mv eFa/lib-eFa-Configure/* $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/eFa-Configure
mv eFa/eFa-Configure $RPM_BUILD_ROOT%{_sbindir}

# Move modules into position
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/selinux
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/token
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/www/html/mailscanner/
mv eFa/eFa-release.php $RPM_BUILD_ROOT%{_localstatedir}/www/html/mailscanner/
mv eFa/eFa-learn.php $RPM_BUILD_ROOT%{_localstatedir}/www/html/mailscanner/
mv eFa/CustomAction.pm $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/token
mv eFa/eFavmtools.te $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/selinux
mv eFa/eFahyperv.te $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/selinux
mv eFa/eFaqemu.te $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/selinux
mv eFa/eFa.fc $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/selinux
mv eFa/eFa9.te $RPM_BUILD_ROOT%{_localstatedir}/eFa/lib/selinux
mv eFa/eFa-Monitor-cron $RPM_BUILD_ROOT%{_sbindir}
mv eFa/eFa-Backup $RPM_BUILD_ROOT%{_sbindir}
mv eFa/eFa-Weekly-DMARC $RPM_BUILD_ROOT%{_sbindir}
mv eFa/eFa-Daily-DMARC $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mv eFa/eFa-Monitor  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/eFa-Monitor
mv eFa/eFa-Tokens.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
mv eFa/eFa-Backup.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
mv eFa/eFa-logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mv eFa/mysqltuner.pl $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_usrsrc}/eFa/mariadb
# Move update scripts into position
mv updates $RPM_BUILD_ROOT%{_usrsrc}/eFa

%pre

%preun

# leave files alone during uninstall (eFa package installs are permanent)

%postun

# leave files alone during uninstall (eFa package installs are permanent)

%post

flag=0
if [ "$1" = "1" ]; then
    # Perform Installation tasks

    # Sanity check in case rpm was removed
    if [[ -e %{_sysconfdir}/eFa-Version ]]; then
        echo "Previous eFa install detected."
        echo "Skipping post phase configuration tasks and executing all updates."
        flag=1
    else
        echo -e "\nPreparing to install eFa"

        /bin/sh %{_usrsrc}/eFa/postfix-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/mailscanner-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/clamav-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/clamav-unofficial-sigs-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/spamassassin-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/apache-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/sqlgrey-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/mailwatch-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/mariadb-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/sgwi-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/pyzor-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/razor-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/dcc-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/unbound-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/opendkim-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/opendmarc-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/yum-cron-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/service-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/eFa-config-5.0.0.sh
        /bin/sh %{_usrsrc}/eFa/eFaInit-config-5.0.0.sh

        echo "eFa-%{version}-%{releasenum}" > %{_sysconfdir}/eFa-Version
        echo "Build completed!"
    fi
fi
if [[ "$1" == "2" || "$flag" == "1" ]]; then
    # Perform Update tasks
    echo -e "\nPreparing to update eFa..."

    # v5 cumulative fixes
    {
      /bin/sh %{_usrsrc}/eFa/updates/update.sh
      [[ $? -ne 0 ]] && echo "Error while updating eFa, Please visit https://efa-project.org to report the commands executed above." && exit 0
    } 2>&1 | tee -a /var/log/eFa/update.log
       
    # cleanup if sucessful
    rm -rf /usr/src/eFa
    echo "eFa-%{version}-%{releasenum}" > %{_sysconfdir}/eFa-Version

    echo "Update completed successfully!"
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{_usrsrc}/eFa
%{_localstatedir}/eFa/lib/eFa-Configure
%attr(0755, root, root) %{_sbindir}/eFa-Configure
%attr(0755, root, root) %{_sbindir}/eFa-Monitor-cron
%config(noreplace) %{_sysconfdir}/sysconfig/eFa-Monitor
%attr(0755, root, root) %{_sbindir}/eFa-Backup
%attr(0755, root, root) %{_sbindir}/mysqltuner.pl
%attr(0755, root, root) %{_sbindir}/eFa-Weekly-DMARC
%attr(0755, root, root) %{_sbindir}/eFa-Daily-DMARC
%attr(0755, root, root) %{_localstatedir}/eFa/lib/selinux/eFavmtools.te
%attr(0755, root, root) %{_localstatedir}/eFa/lib/selinux/eFahyperv.te
%attr(0755, root, root) %{_localstatedir}/eFa/lib/selinux/eFaqemu.te
%attr(0755, root, root) %{_localstatedir}/eFa/lib/selinux/eFa.fc
%attr(0755, root, root) %{_localstatedir}/eFa/lib/selinux/eFa9.te
%attr(0644, root, root) %{_localstatedir}/eFa/lib/token/CustomAction.pm
%attr(0644, root, root) %{_localstatedir}/www/html/mailscanner/eFa-release.php
%attr(0644, root, root) %{_localstatedir}/www/html/mailscanner/eFa-learn.php
%attr(0755, root, root) %{_sysconfdir}/cron.daily/eFa-Backup.cron
%attr(0755, root, root) %{_sysconfdir}/cron.daily/eFa-Tokens.cron
%attr(0644, root, root) %{_sysconfdir}/logrotate.d/eFa-logrotate

%changelog
* Fri Jul 27 2024 eFa-Project <shawniverson@efa-project.org> - 5.0.0-11
- Fix quoting for MailWatchConf.pm

* Fri Jul 26 2024 eFa-Project <shawniverson@efa-project.org> - 5.0.0-10
- Check queues for proper permissions with cron, added rpms by request

* Sat Jul 20 2024 eFa-Project <shawniverson@efa-project.org> - 5.0.0-9
- Fixes to aid in migration from v4 appliance

* Tue Jun 11 2024 eFa Project <shawniverson@efa-project.org> - 5.0.0-8
- Fix MailWatchConf.pm configuration during update

* Sun Jun 09 2024 eFa Project <shawniverson@efa-project.org> - 5.0.0-7
- Update MailWatch and additional cleanup mariadb recovery

* Sun May 12 2024 eFa Project <shawniverson@efa-project.org> - 5.0.0-6
- Add certbot as a dependency for eFa, ensure freshclam is enabled

* Sat Apr 13 2024 eFa Project <shawniverson@efa-project.org> - 5.0.0-5
- Fixes for opendkim and operndmarc socket configuration, spamassassin 4.0.1

* Sat Apr 06 2024 eFa Project <shawniverson@efa-project.org> - 5.0.0-4
- Update MailScanner, MailWatch, use NetworkManager, misc fixes

* Sun Feb 25 2024 eFa Project <shawniverson@efa-project.org> - 5.0.0-3
- Update postfix

* Wed Dec 27 2023 eFa Project <shawniverson@efa-project.org> - 5.0.0-2
- Update MailScanner

* Wed Mar 08 2023 eFa Project <shawniverson@efa-project.org> - 5.0.0-1
- CentOS 9 eFa5

* Sat Mar 04 2023 eFa Project <shawniverson@efa-project.org> - 4.0.4-40
- Add IUS Archive repo for centos7 hosts

* Sun Jul 10 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-39
- Fixes for trusted networks handling

* Tue Jul 05 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-38
- Obsoletes and requires for mariadb104-errmsg

* Tue Jul 05 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-37
- Obsoletes for CentOS 7 mariadb102 rpms

* Mon Jul 04 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-36
- Bump mariadb version for IUS/CentOS7

* Sun Jul 03 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-35
- Require ipcalc for CentOS 8 variants, update unrar and MailScanner

* Tue Apr 12 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-34
- Fix from @freyuh for eFa-learn.php IPv6 and resulting php-gmp requirement

* Sat Mar 19 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-33
- Minor fixes for eFa-Configure, eFa-Post-Init build requirements, and db schema

* Sat Mar 12 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-32
- More Fixes trusted networks dialog 

* Sat Mar 12 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-31
- Fix trusted networks dialog

* Sat Mar 12 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-30
- Inline signature learn fixes

* Sat Mar 12 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-29
- Inline signature release and learn fixes

* Sat Mar 12 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-28
- Inline signature release and learn

* Fri Feb 25 2022 eFa Project <shawniverson@efa-project.org> - 4.0.4-27
- MailScanner update
 
* Thu Nov 25 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-26
- MailScanner update to resolve pipe failures on HTML Disarm

* Sun Nov 21 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-25
- MailWatch update to 1.2.18-5 more relay fixes

* Sun Nov 21 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-24
- MailWatch update to 1.2.18-4 relay fixes

* Tue Nov 16 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-23
- Reapply MailWatch update to 1.2.18-3 unfold message-id

* Mon Nov 15 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-22
- MailWatch update to 1.2.18-2 unfold message-id

* Sun Nov 14 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-21
- mailscanner update to 5.4.2-2

* Sun Nov 14 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-20
- mailwatch and mailscanner update

* Sat Sep 18 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-19
- releasetoken length fix, mailwatch update

* Sat Aug 07 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-18
- Spamassassin 3.4.6, openDMARC schema update, eFa Tokens fixes

* Sun Jul 18 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-17
- Run mysql_upgrade

* Wed Jul 14 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-16
- Obsolete mariadb101u-common,-libs,-errmsg,-config

* Wed Jul 14 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-15
- Obsolete mariadb101u

* Sat Jul 10 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-14
- Upgrade Mariadb and fix Spamassassin

* Thu Jun 17 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-13
- Downgrade incomplete MailWatch Requirement

* Thu Jun 17 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-12
- Fix for OpenDMARC

* Sun Mar 28 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-11
- SELinux updates and fixes for eFa-Commit

* Sun Feb 21 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-10
- Fixes for eFa-Commit and disable yara rules

* Sun Feb 14 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-9
- Re-enable php-fpm following IUS changes

* Sat Feb 13 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-8
- Update dependencies for IUS changes

* Thu Feb 04 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-7
- Overwrite CustomAction.pm during update

* Wed Feb 03 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-6
- Fix CustomAction.pm token generation

* Sun Jan 31 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-5
- Fix SQLGrey initial load and db character set conversion

* Sun Jan 31 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-4
- Tidy up permissions on key files

* Sun Jan 31 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-3
- Fix hang on update for token db creation

* Sun Jan 31 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-2
- Fix error on update for token db creation

* Sat Jan 30 2021 eFa Project <shawniverson@efa-project.org> - 4.0.4-1
- Add spam release logic back to eFa

* Wed Jan 27 2021 eFa Project <shawniverson@efa-project.org> - 4.0.3-19
- Update MailScanner, fix yara rules, sqlgrey unicode, etc.

* Tue Jan 05 2021 eFa Project <shawniverson@efa-project.org> - 4.0.3-18
- Update clamav-unofficial-sigs, MailWatch, cleanup eFaInit view

* Wed Dec 30 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-17
- Revert requirements for php and move development to dev repo

* Sun Dec 27 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-16
- Relax requirements for php in preparation for php upgrades

* Sat Dec 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-15
- Use https for web bug replacement

* Fri Nov 13 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-14
- MailScanner, clamav-unofficial-sigs, eFa updates

* Fri Nov 13 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-13
- MailScanner update for eFa to fix recipient issue

* Sat Nov 01 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-12
- Multiple updates and fixes for eFa

* Sat Oct 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-11
- Fix sample-spam path variable

* Sat Oct 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-10
- Fix quotes on sample-spam path variable

* Sat Oct 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-9
- Fix spacing on sample-spam path variable

* Sat Oct 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-8
- Lower verbosy of Razor during update and fix sample-spam path

* Sat Oct 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-7
- Razor fixes and CentOS 7 unbound backport

* Sat Sep 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-6
- Ensure clamav-freshclam is enabled and started

* Sat Sep 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-5
- Fixes for update script

* Sat Sep 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-4
- Enable mod_negotiation.so for Apache to allow LanguagePriority

* Sat Sep 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-3
- Fix DNS resolution during eFa Initialization

* Sat Sep 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-2
- Fail2ban eFa-Configure

* Sat Sep 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.3-1
- Fail2ban support and eFa-SAClean fix

* Sat Aug 29 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-31
- Include perl-Switch CentOS 8 and include OpenDMARC in restores

* Sun Aug 27 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-30
- SELinux update and MailWatch update

* Sun Aug 23 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-29
- SELinux update

* Sun Aug 23 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-28
- Fix for unbound segfault CentOS 8

* Sun Aug 23 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-27
- SELinux update

* Sat Aug 22 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-26
- SELinux update

* Sat Aug 22 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-25
- Prep for CentOS 8

* Sun Aug 09 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-24
- SELinux update

* Sun Aug 09 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-23
- Write RECURSIVEDNS setting to eFa-Config

* Sun Aug 09 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-22
- Fix RECURSIVEDNS for IP Settings CLI

* Sun Aug 02 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-21
- Additional fixes for IP Settings CLI

* Sun Aug 02 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-20
- Fix settings hostname with IP Settings CLI

* Sun Jul 26 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-19
- Improve IP Settings CLI

* Sun Jul 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-18
- Apply SELinux updates

* Sun Jul 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-17
- SELinux updates

* Sat Jun 06 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-16
- Update MailScanner

* Sat May 03 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-15
- Update MailScanner and MailWatch

* Tue Apr 18 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-14
- Fix for spamassassin symlink

* Tue Apr 14 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-13
- Fix for dns

* Sun Apr 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-12
- Update for MailScanner

* Sun Apr 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-11
- Fix 1x1 spacer

* Sun Apr 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-10
- Update for MailScanner

* Sun Mar 01 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-9
- Disable NetworkManager overriding dns

* Tue Feb 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-8
- Fix sudden package name change in epel repo clamav-server to clamd

* Sat Feb 08 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-7
- Update MailWatchConf.pm after updating MailWatch

* Sat Feb 08 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-6
- Updates for MailWatch

* Wed Feb 05 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-5
- Additional modules for MaxMind DB lookup performance

* Sun Feb 02 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-4
- Fix missed files in packaging

* Sun Feb 02 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-3
- Fix new archive rulesets

* Sun Feb 02 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-2
- Enable RelayCountry plugin for Spamassassin

* Sat Feb 01 2020 eFa Project <shawniverson@efa-project.org> - 4.0.2-1
- Add modules for Spamassassin and GeoIP2

* Sun Jan 26 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-15
- Fix missing rules entries

* Sun Jan 26 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-14
- Detect and run sa-update/sa-compile if needed plus other fixes

* Sat Jan 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-13
- Fix password.rules again during update

* Sat Jan 25 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-12
- Fix password.rules during update

* Sun Jan 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-11
- Fix queue permissions for Mailwatch queue polling

* Sun Jan 19 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-10
- Add MailScanner, Spamssassin, and postfix updates

* Sun Jan 12 2020 eFa Project <shawniverson@efa-project.org> - 4.0.1-9
- Add logic to implement all updates on reinstall

* Mon Dec 30 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-8
- Fix missing ) in update-4.0.1.sh

* Mon Dec 30 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-7
- Redefine password in MailWatchConf.pm after update

* Sun Dec 29 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-6
- Display current maxmind key if present

* Sat Dec 28 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-5
- Fix eFa-Configure maxmind key entry

* Sat Dec 28 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-4
- Fix eFa-Configure maxmind menu option

* Sat Dec 28 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-3
- Fix update script sed

* Sat Dec 28 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-2
- Fix spec file to allow updates

* Fri Dec 27 2019 eFa Project <shawniverson@efa-project.org> - 4.0.1-1
- Updates and Fixes for eFa 4.0.1 <https://efa-project.org>

* Fri Nov 15 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-68
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Nov 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-67
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Aug 18 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-66
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Mon Jul 08 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-65
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Mon Jul 08 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-64
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Jul 07 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-63
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Jul 07 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-62
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 17 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-61
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-60
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-59
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-58
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-57
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-56
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-55
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-54
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-53
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-52
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Mar 03 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-51
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Mar 02 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-50
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Mar 02 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-49
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 23 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-48
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 23 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-47
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 23 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-46
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 23 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-45
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 23 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-44
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Mon Feb 18 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-43
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Mon Feb 18 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-42
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Mon Feb 18 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-41
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Feb 17 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-40
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Feb 17 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-39
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Feb 17 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-38
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-37
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-36
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-35
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-34
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-33
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-32
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-31
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-30
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 16 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-29
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Fri Feb 15 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-28
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Fri Feb 15 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-27
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Fri Feb 15 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-26
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 07 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-25
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 07 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-24
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 02 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-23
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Feb 02 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-22
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Thu Jan 31 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-21
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Thu Jan 31 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-20
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Thu Jan 31 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-19
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Thu Jan 31 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-18
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Thu Jan 31 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-17
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Wed Jan 30 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-16
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Wed Jan 30 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-15
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Wed Jan 30 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-14
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Tue Jan 29 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-13
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Tue Jan 29 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-12
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Tue Jan 29 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-11
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Jan 27 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-10
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Jan 27 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-9
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Wed Jan 23 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-8
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Tue Jan 22 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-7
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Mon Jan 21 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-6
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Jan 20 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-5
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sun Jan 20 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-4
- Updates and Fixes for eFa 4.0.0 <https://efa-project.org>

* Sat Jan 19 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-3
- Split eFa and eFa-base files <https://efa-project.org>

* Sat Jan 19 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-2
- Test LXC building and updating on CentOS7 <https://efa-project.org>

* Sat Jan 19 2019 eFa Project <shawniverson@efa-project.org> - 4.0.0-1
- Initial Build for eFa v4 on CentOS7 <https://efa-project.org>
