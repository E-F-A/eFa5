#!/bin/sh
#-----------------------------------------------------------------------------#
# eFa 5x cumulative updates script
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
instancetype=$(/sbin/virt-what)

retval=0

function execcmd()
{
eval $cmd && [[ $? -ne 0 ]] && echo "$cmd" && retval=1
}

function randompw()
{
  PASSWD=""
  PASSWD=`openssl rand -base64 32`
}
# +---------------------------------------------------+

# sa-update, if needed
if [[ ! -d /var/lib/spamassassin/4.000001 ]]; then
  cmd='sa-update'
  execcmd
  cmd='sa-compile'
  execcmd
fi

# Update SELinux
if [[ $instancetype != "lxc" ]]; then
    cmd='checkmodule -M -m -o /var/eFa/lib/selinux/eFa.mod /var/eFa/lib/selinux/eFa9.te'
    execcmd
    cmd='semodule_package -o /var/eFa/lib/selinux/eFa.pp -m /var/eFa/lib/selinux/eFa.mod -f /var/eFa/lib/selinux/eFa.fc'
    execcmd
    cmd='semodule -i /var/eFa/lib/selinux/eFa.pp'
    execcmd
fi

# Always refresh /root/.my.cnf
cmd='echo "[client]" > /root/.my.cnf'
execcmd
cmd='echo "user=root" >> /root/.my.cnf'
execcmd
cmd="echo \"password=$(grep ^MYSQLROOTPWD /etc/eFa/MySQL-Config | sed -e 's/^.*://')\" >> /root/.my.cnf"
execcmd
cmd='chmod 400 /root/.my.cnf'
execcmd

# Cleanup
cmd='rm -rf /var/www/eFaInit'
[[ -d /var/www/eFaInit ]] && execcmd
cmd='rm -f /usr/sbin/eFa-Init'
[[ -f /usr/sbin/eFa-Init ]] && execcmd
cmd='rm -f /usr/sbin/eFa-Commit'
[[ -f /usr/sbin/eFa-Commit ]] && execcmd

# Run MySQL upgrade script (safe to run more than once)
/bin/mysql_upgrade >/dev/null 2>&1

# Set milter queue permissions
cmd='chown postfix:postfix /var/spool/MailScanner/milterin'
execcmd
cmd='chown postfix:postfix /var/spool/MailScanner/milterout'
execcmd

# Postfix queue permissions
cmd='chown -R postfix:mtagroup /var/spool/postfix/hold'
execcmd
cmd='chown -R postfix:mtagroup /var/spool/postfix/incoming'
execcmd
cmd='chmod -R 750 /var/spool/postfix/hold'
execcmd
cmd='chmod -R 750 /var/spool/postfix/incoming'
execcmd

if [[ -z $(grep smtpd_forbid_bare_newline /etc/postfix/main.cf) ]]; then
    # Protect against SMTP smuggling
    postconf -e "smtpd_forbid_unauth_pipelining = yes"
    postconf -e "smtpd_discard_ehlo_keywords = chunking, silent-discard"
    postconf -e "smtpd_forbid_bare_newline = yes"
    postconf -e "smtpd_forbid_bare_newline_exclusions = \$mynetworks"
fi

if [[ ! -e /etc/sysconfig/eFa-Daily-DMARC ]]; then
  echo 'SENDREPORTS="yes"' > /etc/sysconfig/eFa-Daily-DMARC
fi

# Enable maintenance mode if not enabled
MAINT=0
if [[ -f /etc/cron.d/eFa-Monitor.cron ]]; then
    rm -f /etc/cron.d/eFa-Monitor.cron
    MAINT=1
fi

cmd='systemctl daemon-reload'
execcmd
cmd='systemctl reload httpd'
execcmd
cmd='systemctl reload php-fpm'
execcmd
cmd='systemctl reload postfix'
execcmd
cmd='systemctl restart clamd@scan'
execcmd
cmd='systemctl restart clamav-unofficial-sigs.timer'
execcmd
cmd='systemctl stop sqlgrey'
execcmd
cmd='systemctl stop msmilter'
execcmd
cmd='systemctl stop mailscanner'
execcmd
cmd='systemctl stop mariadb'
execcmd
cmd='systemctl stop postfix_relay'
execcmd
cmd='systemctl stop milter_relay'
execcmd
cmd='systemctl start mariadb'
execcmd
cmd='systemctl start mailscanner'
execcmd
cmd='systemctl start msmilter'
execcmd
cmd='systemctl start sqlgrey'
execcmd
cmd='systemctl enable postfix_relay'
execcmd
cmd='systemctl start postfix_relay'
execcmd
cmd='systemctl enable milter_relay'
execcmd
cmd='systemctl start milter_relay'
execcmd
cmd='systemctl enable clamav-freshclam'
execcmd
cmd='systemctl start clamav-freshclam'
execcmd
cmd='systemctl enable php-fpm'
execcmd
cmd='systemctl start php-fpm'
execcmd


# Disable maintenance mode if disabled during script
if [[ $MAINT -eq 1 ]]; then
    echo "* * * * * root /usr/sbin/eFa-Monitor-cron >/dev/null 2>&1" > /etc/cron.d/eFa-Monitor.cron
fi

exit $retval
