#!/bin/bash
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
fi