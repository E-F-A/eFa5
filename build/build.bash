#!/bin/bash
#-----------------------------------------------------------------------------#
# eFa 5.0.0 build script version 20240609
#-----------------------------------------------------------------------------#
# Copyright (C) 2013~2024 https://efa-project.org
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
#-----------------------------------------------------------------------------#
action=$1
[[ -z $action ]] && action="production" # default to prod if no arg supplied

#-----------------------------------------------------------------------------#
# Install eFa
#-----------------------------------------------------------------------------#
mirror="https://mirrors.efa-project.org"
LOGFILE="/var/log/eFa/build.log"

#-----------------------------------------------------------------------------#
# Set up logging
#-----------------------------------------------------------------------------#
LOGGER='/usr/bin/logger'
HEADER='=============  EFA 4 (EL 8) / 5 (EL 9) BUILD SCRIPT STARTING  ============'

# CREATE LOG FOLDER IF NOT EXISTS
mkdir -p $(dirname "${LOGFILE}")

# TRY TO CREATE LOG FILE IF NOT EXISTS
( [ -e "$LOGFILE" ] || touch "$LOGFILE" ) && [ ! -w "$LOGFILE" ] && echo "Unable to create or write to $LOGFILE"

function logthis() {
    TAG='EFA'
    MSG="$1"
    $LOGGER -t "$TAG" "$MSG"
    echo "`date +%Y.%m.%d-%H:%M:%S` - $MSG"
    echo "`date +%Y.%m.%d-%H:%M:%S` - $MSG" >> $LOGFILE
}

logthis "$HEADER"
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# check if user is root
#-----------------------------------------------------------------------------#
if [ `whoami` == root ]; then
  logthis "Good you are root."
else
  logthis "ERROR: Please become root first."
  logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
  exit 1
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# check if we run CentOS 9
#-----------------------------------------------------------------------------#
OSVERSION=`cat /etc/redhat-release`
if [[ $OSVERSION =~ .*'release 9'.* ]]; then
  logthis "Good you are running CentOS 9 Stream or similar flavor"
  RELEASE=9
elif [[ $OSVERSION =~ .*'release 8'.* ]]; then
  logthis "Good you are running CentOS 8 or similar flavor"
  RELEASE=8
else
  logthis "ERROR: You are not running CentOS 8, CentOS 9 Stream or equivalent"
  logthis "ERROR: Unsupported system, stopping now"
  logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
  exit 1
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Check that SELinux is not disabled (unless it is lxc)
#-----------------------------------------------------------------------------#
if [[ -z $(grep -i 'lxc\|docker' /proc/1/cgroup) ]]; then
    if [[ -f /etc/selinux/config && -n $(grep -i ^SELINUX=disabled$ /etc/selinux/config)  ]]; then
        logthis "ERROR: SELinux is disabled and this is not an lxc container"
        logthis "ERROR: Please enable SELinux and try again."
        logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
        exit 1
    fi
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Check network connectivity
#-----------------------------------------------------------------------------#
logthis "Checking network connectivity"
# use curl to test in case wget not installed yet.
curl -s --connect-timeout 3 --max-time 10 --retry 3 --retry-delay 0 --retry-max-time 30 "${mirror}" > /dev/null
if [[ $? -eq 0 ]]; then
  logthis "OK - $mirror is reachable"
else
  logthis "ERROR: No network connectivity"
  logthis "ERROR: unable to reach $mirror"
  logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
  exit 1
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# have network, install wget if missing
#-----------------------------------------------------------------------------#
rpm -q wget >/dev/null 2>&1
if [ $? -ne 0 ]; then
    logthis "Installing wget"
    yum -y install wget | tee -a $LOGFILE
    if [ $? -eq 0 ]; then
        logthis "wget installed"
    else
        logthis "ERROR: wget installation failed"
        # non-fatal for this script but will cause issues after system configuration
    fi
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Install perl if missing
#-----------------------------------------------------------------------------#
rpm -q perl >/dev/null 2>&1
if [ $? -ne 0 ]; then
    logthis "Installing perl"
    yum -y install perl | tee -a $LOGFILE
    if [ $? -eq 0 ]; then
        logthis "perl installed"
    else
        logthis "ERROR: perl installation failed"
        exit 1
    fi
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Add eFa Repo
#-----------------------------------------------------------------------------#
case "$action" in
    ("testing"|"kstesting"|"testingnoefa")
        if [[ $RELEASE -eq 9 ]]; then
            logthis "Adding eFa CentOS 9 test Repo"
            mkdir -p /usr/src/eFa
            curl -sSL $mirror/rpm/eFa5/centos9/RPM-GPG-KEY-eFa-Project-256 > /usr/src/eFa/RPM-GPG-KEY-eFa-Project-256
            rpm --import /usr/src/eFa/RPM-GPG-KEY-eFa-Project-256
            curl -L $mirror/rpm/eFa5/centos9/eFa5-test.repo -o /etc/yum.repos.d/eFa5-test.repo
        else
            logthis "Adding eFa CentOS 8 Testing Repo"
            mkdir -p /usr/src/eFa
            curl -sSL $mirror/rpm/eFa4/RPM-GPG-KEY-eFa-Project > /usr/src/eFa/RPM-GPG-KEY-eFa-Project
            rpm --import /usr/src/eFa/RPM-GPG-KEY-eFa-Project
            curl -L $mirror/rpm/eFa4/CentOS8/eFa4-centos8-testing.repo -o /etc/yum.repos.d/eFa4-testing.repo
        fi
        ;;
    
    ("dev"|"ksdev"|"devnoefa")
        if [[ $RELEASE -eq 9 ]]; then
            logthis "Adding eFa CentOS 9 Dev Repo"
            mkdir -p /usr/src/eFa
            curl -sSL $mirror/rpm/eFa5/centos9/RPM-GPG-KEY-eFa-Project-256 > /usr/src/eFa/RPM-GPG-KEY-eFa-Project-256
            rpm --import /usr/src/eFa/RPM-GPG-KEY-eFa-Project-256
            curl -L $mirror/rpm/eFa5/centos9/eFa5-dev.repo -o /etc/yum.repos.d/eFa5-dev.repo
        else
            logthis "Adding eFa CentOS 8 Dev Repo"
            mkdir -p /usr/src/eFa
            curl -sSL $mirror/rpm/eFa4/RPM-GPG-KEY-eFa-Project > /usr/src/eFa/RPM-GPG-KEY-eFa-Project
            rpm --import /usr/src/eFa/RPM-GPG-KEY-eFa-Project
            curl -L $mirror/rpm/eFa4/CentOS8/eFa4-centos8-dev.repo -o /etc/yum.repos.d/eFa4-dev.repo
        fi
        ;;

    *)  if [[ $RELEASE -eq 9 ]]; then
            logthis "Adding eFa CentOS 9 Release Repo"
            mkdir -p /usr/src/eFa
            curl -sSL $mirror/rpm/eFa5/centos9/RPM-GPG-KEY-eFa-Project-256 > /usr/src/eFa/RPM-GPG-KEY-eFa-Project-256
            rpm --import /usr/src/eFa/RPM-GPG-KEY-eFa-Project-256
            curl -L $mirror/rpm/eFa5/centos9/eFa5-release.repo -o /etc/yum.repos.d/eFa5-release.repo
        else
            logthis "Adding eFa Repo"
            mkdir -p /usr/src/eFa
            curl -sSL $mirror/rpm/eFa4/RPM-GPG-KEY-eFa-Project > /usr/src/eFa/RPM-GPG-KEY-eFa-Project
            rpm --import /usr/src/eFa/RPM-GPG-KEY-eFa-Project
            curl -L $mirror/rpm/eFa4/CentOS8/eFa4-centos8.repo -o /etc/yum.repos.d/eFa4.repo
        fi
        ;;
esac
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# epel repo
#-----------------------------------------------------------------------------#
rpm -q epel-release >/dev/null 2>&1
if [ $? -ne 0 ]; then
    logthis "Installing EPEL Repo"
    yum -y install epel-release | tee -a $LOGFILE
    if [ $? -eq 0 ]; then
        logthis "EPEL repo installed"
    else
        logthis "ERROR: EPEL installation failed"
        logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
        exit 1
    fi
fi


if [[ $RELEASE -eq 9 ]]; then
    #-----------------------------------------------------------------------------#
    # crb repo
    #-----------------------------------------------------------------------------#
    rpm -q redhat-release >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        dnf config-manager --set-enabled crb | tee -a $LOGFILE
        if [ $? -eq 0 ]; then
            logthis "crb repo enabled"
        else
            logthis "ERROR: crb repo enable failed"
            logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
            exit 1
        fi
    else
        subscription-manager repos --enable codeready-builder-for-rhel-9-x86_64-rpms
        if [ $? -eq 0 ]; then
            logthis "codeready-builder-for-rhel repo enabled"
        else
            logthis "ERROR: codeready-builder-for-rhel repo enable failed"
            logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
            exit 1
        fi
    fi
    #-----------------------------------------------------------------------------#
    # php 8.1 
    #-----------------------------------------------------------------------------#
    dnf module -y reset php | tee -a $LOGFILE
    if [ $? -ne 0 ]; then
        logthis "ERROR: Reset php dnf module failed"
        logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
        exit 1
    fi
    dnf module -y enable php:8.1 | tee -a $LOGFILE
    if [ $? -eq 0 ]; then
        logthis "php 8.1 stream enabled"
    else
        logthis "ERROR: php 8.1 stream enable failed"
        logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
        exit 1
    fi
else
    logthis "Enabling CentOS 8 PowerTools Repo"
    yum -y install 'dnf-command(config-manager)'
    yum config-manager --set-enabled powertools
    [ $? -ne 0 ] && exit 1
fi

#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Update OS
#-----------------------------------------------------------------------------#
logthis "Updating the OS"
yum -y update | tee -a $LOGFILE
if [ $? -eq 0 ]; then
    logthis "System Updated"
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Remove not needed packages
#-----------------------------------------------------------------------------#
logthis "Removing conflicting packages"
yum -y remove postfix >/dev/null 2>&1
# Ignore return here
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# install eFa
#-----------------------------------------------------------------------------#
logthis "Installing eFa packages (This can take a while)"
rpm -q eFa >/dev/null 2>&1
if [ $? -ne 0 ]; then
    if [[ "$action" != "testingnoefa" && "$action" != "devnoefa" ]]; then
        yum -y install eFa | tee -a $LOGFILE
        if [ $? -eq 0 ]; then
            logthis "eFa Installed"
        else
            logthis "ERROR: eFa failed to install"
            logthis "^^^^^^^^^^ SCRIPT ABORTED ^^^^^^^^^^"
            exit 1
        fi
    fi
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# kickstart
#-----------------------------------------------------------------------------#
if [[ "$action" == "kstesting" || "$action" == "ksproduction" || "$action" == "ksdev" ]]; then
  # Set root default pass for kickstart builds
  echo 'echo "First time login: root/eFaPr0j3ct" >> /etc/issue' >> /etc/rc.d/rc.local
  echo "root:eFaPr0j3ct" | chpasswd --md5 root

  # Disable ssh for kickstart builds
  systemctl disable sshd
fi

if [[ "$action" == "ksproduction" ]]; then
  # Zero free space in preparation for export
  logthis "Zeroing free space"
  dd if=/dev/zero of=/filler bs=4096 >/dev/null 2>&1
  rm -f /filler
  dd if=/dev/zero of=/tmp/filler bs=4096 >/dev/null 2>&1
  rm -f /tmp/filler
  dd if=/dev/zero of=/boot/filler bs=4096 >/dev/null 2>&1
  rm -f /boot/filler
  dd if=/dev/zero of=/var/filler bs=4096 >/dev/null 2>&1
  rm -f /var/filler
  logthis "Zeroed free space"
fi
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# finalize
#-----------------------------------------------------------------------------#
logthis "============  EFA BUILD SCRIPT FINISHED  ============"
logthis "============  PLEASE REBOOT YOUR SYSTEM   ============"

if [[ "$action" == "testing" || "$action" == "production" || "$action" == "dev" ]]; then
  read -p "Do you wish to reboot the system now? (Y/N): " yn
  if [[ "$yn" == "y" || "$yn" == "Y" ]]; then
    shutdown -r +1 "Installation requires reboot. Restarting in 1 minute"
    exit 0
  else
    exit 0
  fi
fi
exit 0
#-----------------------------------------------------------------------------#
