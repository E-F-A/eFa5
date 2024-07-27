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
    cmd='postconf -e "smtpd_forbid_unauth_pipelining = yes"'
    execcmd
    cmd='postconf -e "smtpd_discard_ehlo_keywords = chunking, silent-discard"'
    execcmd
    cmd='postconf -e "smtpd_forbid_bare_newline = yes"'
    execcmd
    cmd='postconf -e "smtpd_forbid_bare_newline_exclusions = \$mynetworks"'
    execcmd
fi

if [[ ! -e /etc/sysconfig/eFa-Daily-DMARC ]]; then
  echo 'SENDREPORTS="yes"' > /etc/sysconfig/eFa-Daily-DMARC
fi

# Ensure MailWatchConf.pm is updated
if [[ -z $(grep MAILWATCHSQLPWD /usr/share/MailScanner/perl/custom/MailWatchConf.pm) ]]; then
  cmd="sed -i \"/^my (\\\$db_pass) =/ c\my (\\\$fh);\nmy (\\\$pw_config) = '/etc/eFa/MailWatch-Config';\nopen(\\\$fh, \\\"<\\\", \\\$pw_config);\nif(\!\\\$fh) {\n  MailScanner::Log::WarnLog(\\\"Unable to open %s to retrieve password\\\", \\\$pw_config);\n  return;\n}\nmy (\\\$db_pass) = grep(/^MAILWATCHSQLPWD/,<\\\$fh>);\n\\\$db_pass =~ s/MAILWATCHSQLPWD://;\n\\\$db_pass =~ s/\\\\\n//;\nclose(\\\$fh);\" /usr/share/MailScanner/perl/custom/MailWatchConf.pm"
  execcmd
  # Also upgrade the db, just in case
  cmd='/usr/bin/mailwatch/tools/upgrade.php --skip-user-confirm /var/www/html/mailscanner/functions.php'
  execcmd
fi 

# Fix duplicate jail configs
if [[ -f /etc/fail2ban/jail.d/jail.local ]]; then
  if [[ -f /etc/fail2ban/jail.d/efa.local ]]; then
    cmd='rm -f /etc/fail2ban/jail.d/jail.local;'
    execcmd
  else 
    cmd='mv /etc/fail2ban/jail.d/jail.local /etc/fail2ban/jail.d/efa.local'
    execcmd
  fi
fi

# Fix symlink and ensure passwords consistent
if [[ ! -h /etc/mail/spamassassin/mailscanner.cf ]]; then
  if [[ -f /etc/MailScanner/spamassassin.conf ]]; then
    if [[ -f /etc/mail/spamassassin/mailscanner.cf ]]; then
      rm -f /etc/MailScanner/spamassassin.conf.bak >/dev/null 2>&1
      cmd='mv /etc/MailScanner/spamassassin.conf /etc/MailScanner/spamassassin.conf.bak'
      execcmd
      cmd='mv /etc/mail/spamassassin/mailscanner.cf /etc/MailScanner/spamassassin.conf'
      execcmd
      if [[ $instancetype != "lxc" ]]; then
        cmd='chcon -t mscan_etc_t /etc/MailScanner/spamassassin.conf'
        execcmd
      fi
    fi
    cmd='ln -s /etc/mail/spamassassin/mailscanner.cf /etc/MailScanner/spamassassin.conf'
    execcmd
    SAUSERSQLPWD="`grep SAUSERSQLPWD /var/eFa/backup/backup/etc/eFa/SA-Config | sed 's/.*://'`"
    cmd="sed -i \"/^bayes_sql_password/ c\bayes_sql_password              $SAUSERSQLPWD\" /etc/MailScanner/spamassassin.conf"
    execcmd
    cmd="sed -i \"/^    user_awl_sql_password/ c\    user_awl_sql_password           $SAUSERSQLPWD\" /etc/MailScanner/spamassassin.conf"
    execcmd
    SAUSERSQLPWD=
  fi
fi

# Create script to reset access
if [[ ! -e /usr/sbin/checkqueues ]]; then
  cat > /usr/sbin/checkqueues << 'EOF'
#!/bin/bash
if [[ $(stat -c '%G' /var/spool/postfix/incoming) != 'mtagroup' ]]; then
    chown -R postfix:mtagroup /var/spool/postfix/incoming
    chmod -R 750 /var/spool/postfix/incoming
fi
if [[ $(stat -c '%G' /var/spool/postfix/hold) != 'mtagroup' ]]; then
    chown -R postfix:mtagroup /var/spool/postfix/hold
    chmod -R 750 /var/spool/postfix/hold
fi
EOF

  cmd='chmod +x /usr/sbin/checkqueues'
  execcmd

# Create a cron to reset access to queues in case postfix updates
  cat > /etc/cron.d/checkqueues << 'EOF'
* * * * * root /usr/sbin/checkqueues
EOF
fi

# Loosen Serializer cache
cmd='chmod 775 /var/www/html/mailscanner/lib/htmlpurifier/standalone/HTMLPurifier/DefinitionCache/Serializer'
execcmd
cmd='chgrp apache /var/www/html/mailscanner/lib/htmlpurifier/standalone/HTMLPurifier/DefinitionCache/Serializer'
execcmd

# Ensure mailwatch permissions are correct for images and tmp
cmd='chgrp -R apache /var/www/html/mailscanner/images'
execcmd
cmd='chgrp -R apache /var/www/html/mailscanner/temp'
execcmd

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
cmd='systemctl enable clamav-freshclam'
execcmd
cmd='systemctl start clamav-freshclam'
execcmd

# Disable maintenance mode if disabled during script
if [[ $MAINT -eq 1 ]]; then
    echo "* * * * * root /usr/sbin/eFa-Monitor-cron >/dev/null 2>&1" > /etc/cron.d/eFa-Monitor.cron
fi

exit $retval
