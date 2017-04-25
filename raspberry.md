# Installing a raspberry pi from scratch

For this project, we make primary use of the Raspberry Pi model 3. In order to have a 
consistant method and starting point, please use this cheat sheet to setup and configure your pi.

## Use the right image

https://www.raspberrypi.org/downloads/raspbian/

Use the lite version: `2017-04-10-raspbian-jessie-lite.zip` and unzip it of course

## Flash a new card with a mac ( sorry PC folks )

You'll be using a mini-sd card, and you'll insert that into your mac using either a SD card adapter, or a USB adapter

Follow these instructions: https://www.raspberrypi.org/documentation/installation/installing-images/mac.md

Which are roughly:

```
diskutil list
diskutil unmountDisk /dev/disk2
sudo dd bs=1m if=2017-04-10-raspbian-jessie-lite.img of=/dev/rdisk2
```

## Add the ssh file

After the drive is finished with the dd, you'll see a drive called "boot" show up on your mac. In order to enable SSH by default,
you need to copy a small, empty file called `ssh` onto the disk, or `touch` to make an empty file. If you forget this,
you'll have to hook the PI to a keyboard and a monitor which is really annoying!

## Unmount again, safely

Either use the UI, or execute `diskutil unmountDisk /dev/disk2` again

## Boot the pi and follow this checklist:

- `sudo vi /etc/motd` because the default motd is ugly and it's great to know which pi
- `sudo apt-get update ; sudo apt-get upgrade`
- `sudo raspi-config`
-- Change the password to something like `paranoia`
-- Change the hostname to something you like
-- Set the boot to headless / command prompt
-- Localization: set the wifi country to US, change the character set to en.US-UTF8 and remove the UK thing
-- Interfacing: enable I2C but none of the others, turn on SSH if you are paranoid
-- Advanced: expand the file system, set the memory split to 16M

## If you're going to use git locally for development

`sudo apt-get install git`

`ssh-keygen`

`cat .ssh/id_rsa.pub` 
Copy this into Github in the standard way. 

`git clone git@github.com:bbulkow/MagnusFlora`


## Reboot and you should see all is good
