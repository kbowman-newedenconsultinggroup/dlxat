creating usb

for f in `ls /media/kbowman/` ; do rsync -avz --del . /media/kbowman/$f/. ;done
