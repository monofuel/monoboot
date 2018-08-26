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

    config.vm.synced_folder './', '/mnt/vagrant/', type: 'nfs', nfs_version: 4, nfs_udp: false
    config.vm.provision "shell", inline: <<-SHELL
        export DEBIAN_FRONTEND=noninteractive
        apt update
        apt install dirmngr

        echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main' > /etc/apt/sources.list.d/ansible.list
        apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
        apt update
        apt install wget curl git vim tmux htop make -y
        apt install debootstrap squashfs-tools -y
        apt install ansible -y

        mkdir /chroots
        make chroots

    SHELL
end
