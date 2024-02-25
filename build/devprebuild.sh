#!/bin/bash
######################################################################
# eFa 5.0.0 Development prebuild environment
######################################################################
# Copyright (C) 2024  https://efa-project.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# Git path
GITPATH="/root/eFa5"

# check if user is root
if [ `whoami` == root ]; then
  echo "Good you are root."
else
  echo "ERROR: Please become root first."
  exit 1
fi

# check if we run CentOS 9
OSVERSION=`cat /etc/redhat-release`
if [[ $OSVERSION =~ .*'release 9'.* ]]; then
  logthis "Good you are running CentOS 9 or similar flavor"
  RELEASE=9
else
  echo "- ERROR: You are not running CentOS 9 or similar flavor"
  echo "- ERROR: Unsupported system, stopping now"
  exit 1
fi

if [[ -f /etc/selinux/config && -n $(grep -i ^SELINUX=disabled$ /etc/selinux/config)  ]]; then
  echo "- ERROR: SELinux is disabled and this is not an lxc container"
  echo "- ERROR: Please enable SELinux and try again."
  exit 1
fi

if [[ ! -d /root/eFa5 ]]; then
  echo "- ERROR: git path is incorrect"
  echo "- ERROR: Please clone to /root/eFa5 or update GITPATH and try again."
  exit 1
fi

dnf -y install epel-release
[ $? -ne 0 ] && exit 1

dnf config-manager --set-enabled crb

dnf -y update
[ $? -ne 0 ] && exit 1

dnf -y install rpm-build
[ $? -ne 0 ] && exit 1

mkdir -p $GITPATH/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
[ $? -ne 0 ] && exit 1
echo "%_topdir $GITPATH/rpmbuild" > ~/.rpmmacros
[ $? -ne 0 ] && exit 1
cd $GITPATH/rpmbuild/SPECS
[ $? -ne 0 ] && exit 1

