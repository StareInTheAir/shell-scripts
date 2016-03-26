## btrfs
### Create
	mkfs.btrfs -m raid1 -d raid5 /dev/sdc /dev/sdd /dev/sde /dev/sdf

RAID levels for metadata and real data can be set differently

### Mount
	mkdir /media/btrRAID
	mount /dev/sda /media/btrRAID/
	
### Ummount
	umount /media/btrRAID/

### mount on boot

``/etc/fstab``:

	UUID=d0f61c46-ced0-42c9-b28e-26f07c3474d9       /media/btrRAID  btrfs   nofail 0 0

#### UUID
	blkid
	lsblk --fs

### Show infos
	btrtf filesystem show /media/btrfsRAID/

	# df doesn't work correctly with btrfs
	btrfs filesystem df /media/btrRAID/

	# More detailed
	btrfs device usage /media/btrRAID/
	
	# Error count
	btrfs dev stats /media/btrRAID/

### Add volume
	btrfs device add /dev/sdc /media/btrRAID/


Then a balance needs to happens, to distribute data onto new drive

	btrfs filesystem balance /media/btrRAID/


Status can be viewed with
	
	btrfs balance status /media/btrRAID/
	watch -n 10 btrfs balance status /media/btrRAID/


Balance can be canceled with

	btrfs balance cancel /media/btrRAID/	

### Change RAID level
	btrfs balance start -dconvert=raid0 -mconvert=raid0 /media/btrRAID

### Create subvolume
	btrfs subvolume create /media/btrRAID/backup
Has to be on a btrfs mount point

### List subvolumes
	btrfs subvolume list /media/btrRAID/

### Snapshots
	btrfs subvolume snapshot /media/btrRAID/ /media/btrRAID/2015-12-26-10-04_snapshot-name
First param is source, second is target

#### Snapshot strategy
	# Mount root of btrfs volume at /media
	mount /dev/sdg3 /media/btrfs

	# create a snapshot subvolume
	btrfs sub create /media/btrfs/snapshots

	# create a directory for each subvolume to snapshot in snapshots/
	mkdir /media/btrfs/snapshots/root
	mkdir /media/btrfs/snapshots/home
	
	# mount snapshots subvolume at /snapshots
	mount /dev/sdg3 /snapshots -o subvol=/snapshots

	# create from time to time readonly snapshots in /snapshots
	btrfs subvol snap -r / /snapshots/root/2016-04-01-17-12_title-of-snapshot
	btrfs subvol snap -r /home /snapshots/home/2016-04-01-17-12_title-of-snapshot
	
	# restore snapshot
	# Assume fuck up in /home
	umount /home
	mount /dev/sdg3 /media/btrfs
	mv /media/btrfs/home /media/btrfs/home-fucked-up # = rename of subvolume
	# create new writeable snapshot of snapshot at home
	btrfs subvol snap /media/btrfs/snapshots/home/2016-04-01-17-12_title-of-snapshot /media/btrfs/home
	btrfs subvol delete /media/btrfs/home-fucked-up
	mount /dev/sdg3 /home -o subvol=/home

#### Resources
- https://btrfs.wiki.kernel.org/index.php/SysadminGuide#Snapshots
- http://unix.stackexchange.com/a/46384
