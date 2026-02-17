import os
import sys
import tomllib

if os.geteuid() != 0:
    print("Error: This script must be run as root.", file=sys.stderr)
    sys.exit(1)

UDEV_CAMERA_RULES_FILE = "/etc/udev/rules.d/99-camera.rules"
UDEV_PRINTER_RULES_FILE = "/etc/udev/rules.d/99-thermal-printer.rules"

with open("devices.toml", "rb") as f:
    config = tomllib.load(f)

camera_config = config["devices"]["camera"]
if not camera_config:
    raise ValueError("No camera configuration found in devices.toml")
printer_config = config["devices"]["printer"]
if not printer_config:
    raise ValueError("No printer configuration found in devices.toml")


def write_rule(file, rule):
    with open(file, "w") as f:
        f.write(rule)
    print(f"Udev rules written to {file}:\n{rule}")


def get_vid_pid(config):
    vid = config["vendor_id"].lower().replace("0x", "")
    pid = config["product_id"].lower().replace("0x", "")
    return vid, pid


# ------------------------------ Camera config ---------------------------------

vid, pid = get_vid_pid(camera_config)
symlink = camera_config["device"]
rule = f'SUBSYSTEM=="video4linux", ATTRS{{idVendor}}=="{vid}", ATTRS{{idProduct}}=="{pid}", KERNEL=="video*", ATTR{{index}}=="0", SYMLINK+="{symlink.replace('/dev/', '')}"\n'
write_rule(UDEV_CAMERA_RULES_FILE, rule)

# ------------------------------ Printer config --------------------------------

vid, pid = get_vid_pid(printer_config)
rule = f'SUBSYSTEM=="usb", ATTR{{idVendor}}=="{vid}", ATTR{{idProduct}}=="{pid}", MODE="0666"\n'
write_rule(UDEV_PRINTER_RULES_FILE, rule)
