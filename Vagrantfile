# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.hostname = "pxe"
    config.vm.box = "debian/stretch64"
    config.vm.provider :libvirt do |libvirt|
        libvirt.cpus = 4
        libvirt.memory = 2048
    end
    config.vm.network :public_network, :bridge => 'enp5s0', :dev => 'enp5s0'

    config.vm.synced_folder './web', '/mnt/web/', type: 'nfs', nfs_version: 4, nfs_udp: false
    config.vm.provision "shell", inline: <<-SHELL
        export DEBIAN_FRONTEND=noninteractive
        apt update
        apt install wget curl git vim tmux htop -y
        apt install debootstrap squashfs-tools -y

        # https://djlab.com/2014/10/debian-pxe-boot-image-from-scratch/

    SHELL
end
