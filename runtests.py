#!/usr/bin/python
import subprocess
import os
import time

insmod = subprocess.Popen(['/usr/sbin/insmod', '/home/runner/work/openrazer/openrazer/driver/razerkbd.ko'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
insmod_tee = subprocess.Popen(['/usr/bin/tee', '/tmp/output-insmod'], stdin=insmod.stdout)

env = os.environ.copy()
env['PYTHONUNBUFFERED'] = "1"

print(env)

udevd = subprocess.Popen(['/lib/systemd/systemd-udevd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
udevd_tee = subprocess.Popen(['tee', '/tmp/output-udevd'], stdin=udevd.stdout)

openrazer_daemon = subprocess.Popen(['/usr/bin/openrazer-daemon', '--as-root', '-F'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
openrazer_daemon_tee = subprocess.Popen(['tee', '/tmp/output-openrazer-daemon'], stdin=openrazer_daemon.stdout)

for device in ('razer_blackwidow_ultimate_2012', 'razer_huntsman_mini_analog', 'razer_anansi', 'razer_blackwidow_v3_mini_hyperspeed', 'razer_blackwidow_v3_mini_hyperspeed_wireless', 'razer_blackwidow_v3_pro_wired', 'razer_huntsman_v2'):
    razer_emulator = subprocess.Popen(['/opt/pipx_bin/razer-emulator', '--device', device], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    razer_emulator_tee = subprocess.Popen(['/usr/bin/tee', '/tmp/output-razer-emulator'], stdin=razer_emulator.stdout)

    time.sleep(7)

    functional_tests = subprocess.Popen(['python3', '/home/runner/work/openrazer/openrazer/examples/functional_tests.py', 'noprompt'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    functional_tests_tee = subprocess.Popen(['tee', '/tmp/output-functional-tests'], stdin=functional_tests.stdout)

    functional_tests.wait()

    razer_emulator.terminate()

udevd.terminate()
openrazer_daemon.terminate()
functional_tests.terminate()

print(subprocess.check_output(["ls", '/var/log']))
