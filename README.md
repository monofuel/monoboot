# Monoboot

ipxe configs for booting on my home network

on OpenWRT, enable the TFTP server in DHCP and DNS settings. set the TFTP server root to /usr/lib/tftpboot and the image to mono.kpxe. run make mono.kpxe on the dev machine and copy it to /usr/lib/tftpboot on the openwrt server.

point nginx on the tftp server to the web folder in this repo
