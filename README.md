creating usb

for f in `ls /media/kbowman/` ; do echo ;echo "*** $f ***"; echo ;rsync -avz --del . /media/kbowman/$f/. ;done
