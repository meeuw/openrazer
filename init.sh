#!/bin/bash
mount -t proc procfs /proc
mount -t sysfs sysfs /sys
mount -t configfs configfs /sys/kernel/config
mount -t debugfs debugfs /sys/kernel/debug
mount -t tmpfs tmpfs /run

XDG_DATA_HOME=/home/runner/.local XDG_CONFIG_HOME=/home/runner/.config/ dbus-run-session -- python3 /home/runner/work/openrazer/openrazer/runtests.py|tee /tmp/output-runtests

sleep 2

cp /sys/kernel/debug/gcov/home/runner/work/openrazer/openrazer/driver/*.gcno /tmp
cp /sys/kernel/debug/gcov/home/runner/work/openrazer/openrazer/driver/*.gcda /tmp

/sbin/halt -f
