cp ./keyboardpy.service /etc/systemd/system/keyboardpy.service
cp fix-numlock/fix-numlock.sh /usr/local/bin/fix-numlock
cp fix-numlock/fix-numlock.service /etc/systemd/system/fix-numlock.service
cp fix-numlock/99-fix-numlock.rules /etc/udev/rules.d/99-fix-numlock.rules
systemctl daemon-reload
systemctl enable --now keyboardpy.service
# systemctl enable --now fix-numlock.service
sudo udevadm control --reload-rules
sudo udevadm trigger
