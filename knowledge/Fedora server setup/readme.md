# Fedora setup
- for NAS running Fedora 23 x64 Server Edition Netinstall

## Installation
- Select "minimal" configuration and no additional packages
- Set keyboard layout to german
- Set language to EN/US
- Set hostname in network configuration
- Use custom partitioning and select btrfs option, then auto create
	- Existing partitions may not be deleted, if Fedora was installed before
	- Wipe all partitions with boot CD to be sure
- It takes some time for some options to become available, because data needs to be fetch from network and disks need to be scanned

## Package manager
``dnf``

### update / upgrade
	dnf upgrade

### install	
	dnf install <package>

	
## SSH
- Setup, so only public / private key authentication works
- With ``ssh-copy-id -i clientkey.pub user@server`` copy public keys from clients to server
- In ``/etc/ssh/sshd_config`` set

		PermitRootLogin        prohibit-password
		PasswordAuthentication no
		GSSAPIAuthentication   no

- ``systemctl restart sshd``

## Cockpit
https://server-hostname:9090/

- Does not work in Safari on OSX
	- tested with Safari 9.0.1 on OSX 10.11.1
	- possibly future versions too
- SSH keys for each user can be edited here

## Encrypted mdadm RAID
### Mount
	mkdir /media/decRAID
	cryptsetup luksOpen /dev/vgRAID5/lvRAID5 decRAID
	mount --read-only /dev/mapper/decRAID /media/decRAID

### Unmount
	umount /media/decRAID
	cryptsetup luksClose /dev/mapper/decRAID

## hdparm
``/etc/hdparm.conf``:

	/dev/disk/by-id/ata-WDC_WD30EZRX-00D8PB0_WD-WCC4N0HRL1ZP {
		spindown_time = 4
	}
	/dev/disk/by-id/ata-WDC_WD30EZRX-00MMMB0_WD-WCAWZ2211117 {
		spindown_time = 4
	}
	/dev/disk/by-id/ata-WDC_WD30EZRX-00MMMB0_WD-WCAWZ2256343 {
		spindown_time = 4
	}
	/dev/disk/by-id/ata-WDC_WD30EZRX-00MMMB0_WD-WMAWZ0393226 {
		spindown_time = 4
	}
	/dev/disk/by-id/ata-WDC_WD30EZRX-00SPEB0_WD-WCC4E5PL84DE {
		spindown_time = 4
	}
	/dev/disk/by-id/ata-WDC_WD30EZRX-00SPEB0_WD-WCC4E5PL8LLK {
		spindown_time = 4
	}

TODO

### Resources
- http://linuxundich.de/hardware/festplatten-automatisch-im-betrieb-in-den-standby-schalten/

## Services
	systemctl status  <service-name>
	systemctl start   <service-name>
	systemctl stop    <service-name>
	systemctl restart <service-name>
	systemctl disable <service-name>
	systemctl enable  <service-name>

## Firewall
Service name: ``firewalld.service``


### Show allowed services and ports for default zone
	firewall-cmd --list-all

### Show allowed services and ports for all zones
	firewall-cmd --list-all-zones

### Temporarily add service exception to firewall
	firewall-cmd --add-service <service-name>

### Permanently add service exception to firewall
not applied immediately, firewall needs to restart

	firewall-cmd --permanent --add-service <service-name>

### Add port exception
	firewall-cmd --add-port=2049/udp
	firewall-cmd --add-port=111/tcp

### Restart firewall
	firewall-cmd --reload
	 ||
	systemctl restart firewalld

### Stop firewall
	systemctl stop firewalld

### Disable firewall
	systemctl --now disable firewalld
	systemctl --now disable rolekit
``rolekit`` starts ``firewalld``, if not disabled

### Resources
https://fedoraproject.org/wiki/FirewallD#Which_zones_are_available.3F

## NFS

###Make firewall exceptions
	firewall-cmd --permanent --add-service=rpc-bind --add-service=mountd --add-service=nfs
	firewall-cmd --reload

### Permissions
 To sort out correct permission on write, use ``bindfs``. Files should have ``rw-rw----`` with group ``users``, directory should have ``rwxrwx---`` with group ``users``

	bindfs --perms=0000:a=rwD --create-for-group=users --create-with-perms=0000:u+rwD:g+rwD /media/btrRAID/ /media/btrRAIDwrite/
	bindfs -r --perms=0000:a=rD /media/btrRAID/ /media/btrRAIDread/

- ``--perms=<perms>`` are the permissions, that the client sees (also available would be ``-g <group>``and ``-u <user>`` to fake ownership of all files and directories, this isn't necessary, because ``others`` have all rights)
- ``-r`` for true read-only mount
- ``--create-for-user=<user>``, ``--create-for-group=<group>`` and ``--create-with-perms=<perms>`` are for the real permission written to the original disk


### /etc/exports

	/media/btrRAIDread   192.168.1.0/24(ro,insecure,fsid=56372)
	/media/btrRAIDwrite  hostname-client1(rw,insecure,fsid=56373) hostname-client2(rw,insecure,fsid=56373)

- ``insecure`` is necessary, because ports above 1024 are used (by default?)
- hostnames can be fake and therefore write access gained, but I am alone in my network [as far as I know]
- ``fsid`` is necessary, because the shares are both bindfs mounts

### Resources

- nfs
	- https://fedoraproject.org/wiki/User:Renich/HowTo/NFSv4
	- http://www.server-world.info/en/note?os=Fedora_23&p=nfs
- bindfs
	- http://linux-club.de/forum/viewtopic.php?t=117539


## SELinux
### Disable
#### At runtime
	setenforce Permissive

#### At boottime (persistent) 
In ``/etc/selinux/config`` do following and restart

	# SELINUX= can take one of these three values:
	#     enforcing - SELinux security policy is enforced.
	#     permissive - SELinux prints warnings instead of enforcing.
	#     disabled - No SELinux policy is loaded.
	SELINUX=disabled


### Get state
	sestatus

### Get all config parameters
	getsebool -a
	

## Samba
	dnf install samba
	systemctl enable smb nmb
	systemctl start smb nmb

### clean config file of comments
	grep "^[^#;]" /etc/samba/smb.conf > etc/samba/smb.conf.clean

### change primary group of user
	usermod -g group user

### add user to supplementary group
	usermod -aG group user
	# or
	gpasswd --add user group

### Enable public read access
#### Create nobody user
	useradd --system --shell /sbin/nologin --gid nobody --home-dir / --no-user-group -M smbnobody

``/etc/samba/smb.conf``:

	map to guest = Bad User
	guest account = smbnobody

	[Share]
		guest ok = yes


### Add exception to firewall
	firewall-cmd --permanent --add-service=samba
	firewall-cmd --reload

### Get SELinux params
	getsebool -a | grep samba
	getsebool -a | grep smb

### Set SELinux params
On each shared file and directory:

	chcon -t samba_share_t <dirs/files>

Remove them again:

	restorecon <dirs/files>

### Resources
- https://wiki.centos.org/HowTos/SetUpSamba
- https://docs.fedoraproject.org/en-US/Fedora/23/html/System_Administrators_Guide/ch-File_and_Print_Servers.html#sect-Samba-Configuring_a_Samba_Server

## Syncthing
	dnf copr enable decathorpe/syncthing
	dnf install syncthing

### Start

**_VERY IMPORTANT_**: To run any ``systemctl --user`` command, you need to be really logged in as the user you want to run the service as. ``su`` and even ``su -`` don't work, because dbus doesn't want to play along then. You either need to be logged in at the physical machine or ``ssh`` to the user.

	systemctl --user enable syncthing
	systemctl --user start syncthing

### Disable syncthing-inotify
The systemd script from decathorpe/syncthing don't uncouple syncthing and syncthing-inotify. You can't uninstall one without the other and they always start in union, even when syncthing-inotify is disabled. To disable syncthing-inotify for good:

	systemctl --user mask syncthing-inotify

### Show logs
	journalctl --user-unit=syncthing
	journalctl --user-unit=syncthing -b # only logs since last reboot

### Resources
- https://copr.fedorainfracloud.org/coprs/decathorpe/syncthing/

## DNF automatic
	dnf install dnf-automatic
	systemctl cat dnf-automatic.timer

### monitor logs	
TODO