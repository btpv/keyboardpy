echo 'ACTION=="add", SUBSYSTEM=="input", ENV{ID_INPUT_KEYBOARD}=="1", TAG+="systemd", ENV{SYSTEMD_WANTS}+="fix-numlock.service"' > /etc/udev/rules.d/99-fix-numlock.rules
echo '#!/bin/bash
shopt -s nullglob

leds=(/sys/class/leds/*::numlock/brightness)

any_on=false
all_on=true

if ((${#leds[@]} == 0)); then
    exit 1
fi

for led in "${leds[@]}"; do
    if [[ $(<"$led") == 1 ]]; then
        any_on=true
    else
        all_on=false
    fi
done

if [[ "$any_on" != "$all_on" ]]; then
    echo "Fixing NumLock state: $any_on != $all_on"

    for led in "${leds[@]}"; do
        echo "$([[ "$any_on" == true ]] && echo 1 || echo 0)" > "$led"
    done
fi' > /usr/local/bin/fix-numlock
chmod +x /usr/local/bin/fix-numlock
echo '[Unit]
Description=Fix inconsistent NumLock LED state

[Service]
Type=oneshot
ExecStart=/usr/local/bin/fix-numlock' > /etc/systemd/system/fix-numlock.service

systemctl daemon-reload
udevadm control --reload-rules
udevadm trigger
