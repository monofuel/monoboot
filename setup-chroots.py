#!/usr/bin/python3

# setup script assumes root

from typing import List
import subprocess
import json
import os
import re
from shutil import copyfile
from os import listdir, path

# https://djlab.com/2014/10/debian-pxe-boot-image-from-scratch/
# TODO use ansible's new python stuff rather than subprocess

def debug(text: str):
  try:
    if os.environ['DEBUG'] == 'true':
      print('DEBUG: ' + text) 
  except KeyError:
    return

def list_chroots() -> List[str]:
  debug('listing chroots')
  chroots_output = subprocess.getoutput('ansible-inventory --list')
  chroots = json.loads(chroots_output)
  return chroots['chroots']['hosts']

def bootstrap(chroot: str):
  if (os.path.isdir(chroot)):
    print('chroot {} exists, skipping debootstrap'.format(chroot))
    return
  print('bootstrapping ' + chroot)
  subprocess.run('debootstrap --arch=amd64 stable ' + chroot, shell=True)

def chroot_command(chroot: str, command: str):
  command = 'chroot {} /bin/bash -c "{}"'.format(chroot, command)
  debug(command)
  subprocess.run(command, shell=True)

def chroot_prep(chroot: str):
  subprocess.run('mount -t proc proc {}/proc'.format(chroot), shell=True)
  subprocess.run('mount -t sysfs sys {}/sys'.format(chroot), shell=True)
  subprocess.run('mount -o bind /dev {}/dev'.format(chroot), shell=True)
  chroot_command(chroot, 'apt update')
  chroot_command(chroot, 'apt upgrade -y')
  chroot_command(chroot, 'apt install python python3 -y')
  print("chroot {} prepped".format(chroot))

def chroot_cleanup(chroot: str):
  #chroot_command(chroot, '')
  chroot_command(chroot, 'apt clean')
  chroot_command(chroot, 'rm -rf /tmp/*')
  subprocess.run('umount -f  {}/proc'.format(chroot), shell=True)
  subprocess.run('umount -f  {}/sys'.format(chroot), shell=True)
  subprocess.run('umount -f  {}/dev'.format(chroot), shell=True)
  print("chroot {} cleaned up".format(chroot))

def setup_pxe(chroot: str):
  # copy vmlinuz and initrd
  boot_path = path.join(chroot, 'boot')
  boot_files =  [f for f in listdir(boot_path) if path.isfile(path.join(boot_path, f))]
  # figure out what the newest files are
  vmlinuz_files = [f for f in boot_files if re.match(r'^vmlinuz.*', path.basename(f))]
  initrd_files = [f for f in boot_files if re.match(r'^initrd.*', path.basename(f))]
  # TODO assert lists are not empty
  vmlinuz_file = path.join(boot_path, sorted(vmlinuz_files)[-1])
  initrd_file = path.join(boot_path, sorted(initrd_files)[-1])

  debug('vmlinuz: {} initrd: {}'.format(vmlinuz_file, initrd_file))

  dst_folder = path.join('/mnt/vagrant/web/', path.basename(chroot));
  if not (os.path.isdir(dst_folder)):
    os.mkdir(dst_folder)
  print('copying files to {}'.format(dst_folder))
  copyfile(vmlinuz_file, path.join(dst_folder, 'vmlinuz'))
  copyfile(initrd_file, path.join(dst_folder, 'initrd.img'))

  # package the squashfs
  print('squashing {}'.format(chroot))
  subprocess.run('mksquashfs {} {} -noappend -e boot'.format(chroot, path.join(dst_folder, 'filesystem.squashfs')), shell=True)


# TODO would be nice to check args choose to build a specific chroot
# TODO would be nice to take a flag to force redoing debootstrap
def main():
  chroots = list_chroots()
  debug(str(chroots))
  for chroot in chroots:
    bootstrap(chroot)
    chroot_prep(chroot)

  subprocess.run('ansible-playbook ./playbooks/pxe.yml', shell=True)
  for chroot in chroots:
    chroot_cleanup(chroot)
    setup_pxe(chroot)

if __name__ == "__main__":
  main()