#!/bin/sh
#-----------------------------------------------------------------------------#
# eFa 5.0.0 initial unbound-configuration script
#-----------------------------------------------------------------------------#
# Copyright (C) 2023 https://efa-project.org
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

#-----------------------------------------------------------------------------#
# Start configuration of unbound
#-----------------------------------------------------------------------------#
echo "Configuring unbound..."

# disable validator
#sed -i "/^\tmodule-config:/ c\\\tmodule-config: \"iterator\"" /etc/unbound/unbound.conf

echo "forward-zone:" > /etc/unbound/conf.d/forwarders.conf
echo '  name: "."' >> /etc/unbound/conf.d/forwarders.conf
echo "  forward-addr: 8.8.8.8" >> /etc/unbound/conf.d/forwarders.conf
echo "  forward-addr: 8.8.4.4" >> /etc/unbound/conf.d/forwarders.conf

# Set override to prevent segfault on boot from turning on before networking is ready
mkdir -p /etc/systemd/system/unbound.service.d
echo -e "[Unit]\nAfter=network-online.target\n" > /etc/systemd/system/unbound.service.d/override.conf

echo "Configuring unbound...done"