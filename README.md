# Monoboot

ipxe configs for booting on my home network

on OpenWRT, enable the TFTP server in DHCP and DNS settings. set the TFTP server root to /usr/lib/tftpboot and the image to mono.kpxe. run make mono.kpxe on the dev machine and copy it to /usr/lib/tftpboot on the openwrt server.

point nginx on the tftp server to the web folder in this repo. 

- prepare to bootstrap with `vagrant up`
- `vagrant ssh` then switch to root and browse to /mnt/vagrant and run `make chroots`
- make sure /dev/vdb1 is mounted at /chroots (currently doesn't remount on vagrant up after provisioning)
- `make chroots` generates the chroot environments in /chroots, then copies the vmlinuz and initrd.img to the web folder and generates a squashfs
