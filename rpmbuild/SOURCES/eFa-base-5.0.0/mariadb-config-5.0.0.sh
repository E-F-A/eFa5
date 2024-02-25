#!/bin/sh
#-----------------------------------------------------------------------------#
# eFa 5.0.0 initial mailwatch-configuration script
#-----------------------------------------------------------------------------#
# Copyright (C) 2024 https://efa-project.org
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

#-----------------------------------------------------------------------------#
# Source the settings file
#-----------------------------------------------------------------------------#
source /usr/src/eFa/eFa-settings.inc
#-----------------------------------------------------------------------------#

# Tweak mariadb configuration
# Remove limits on mariadb
mkdir -p /etc/systemd/system/mariadb.service.d
cat > /etc/systemd/system/mariadb.service.d/limit.conf << 'EOF'
[Service]
LimitNOFILE=infinity
LimitMEMLOCK=infinity
EOF

echo -e "[Service]\nTimeoutSec=900\n" > /etc/systemd/system/mariadb.service.d/override.conf

sed -i "/^\[mysqld\]/ a\character-set-server = utf8mb4" /etc/my.cnf.d/mariadb-server.cnf
sed -i "/^\[mysqld\]/ a\init-connect = 'SET NAMES utf8mb4'" /etc/my.cnf.d/mariadb-server.cnf
sed -i "/^\[mysqld\]/ a\collation-server = utf8mb4_unicode_ci" /etc/my.cnf.d/mariadb-server.cnf

  # Performance tweaks
sed -i "/^\[mariadb\]$/ a\bind-address = 127.0.0.1\n\
innodb-defragment = 1 \n\
innodb_buffer_pool_instances = 1 \n\
innodb_buffer_pool_size = 1G \n\
innodb_file_per_table = 1 \n\
innodb_log_buffer_size = 32M \n\
innodb_log_file_size = 125M \n\
join_buffer_size = 512K \n\
key_cache_segments = 4 \n\
max_allowed_packet = 16M \n\
max_heap_table_size = 32M \n\
query_cache_size = 0M \n\
query_cache_type = OFF \n\
read_buffer_size = 2M \n\
read_rnd_buffer_size = 1M \n\
skip-external-locking \n\
skip-host-cache \n\
sort_buffer_size = 4M \n\
thread_cache_size = 16 \n\
tmp_table_size = 32M \n\
skip-name-resolve \n\
skip-host-cache\n" /etc/my.cnf.d/mariadb-server.cnf