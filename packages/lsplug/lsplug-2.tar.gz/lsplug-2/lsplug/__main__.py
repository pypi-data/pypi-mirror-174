import argparse
import glob
import os
import re

from lsplug.helpers import sysfs_str, sysfs_hex, sysfs_int, sysfs_float
from lsplug.hwdata import get_vendor, get_product
import lsplug.query as query


def port_sortable(path):
    port = os.path.basename(path)
    parts = re.split('[-:\.]|usb', port)
    res = []
    for p in parts:
        try:
            res.append(int(p))
        except:
            res.append(0)
    return tuple(res)


def get_ports(filter=None, use_db=True, fixed=False, portinfo=False, devinfo=False, intfinfo=False):
    if len(filter) == 0:
        filter = None

    for port in sorted(glob.glob('/sys/bus/usb/devices/*'), key=port_sortable):
        name = os.path.basename(port)
        if 'usb' in name:
            continue
        if ':' in name:
            continue
        if filter is not None and name not in filter:
            continue
        rem = sysfs_str(port, 'removable')
        if not fixed and rem == "fixed":
            continue
        manufacturer = sysfs_str(port, 'manufacturer')
        product = sysfs_str(port, 'product')
        vid = sysfs_hex(port, "idVendor")
        pid = sysfs_hex(port, "idProduct")
        serial = sysfs_str(port, "serial")
        if serial is None:
            serial = ""
        else:
            serial = f" [{serial}]"
        if use_db:
            db_vendor = get_vendor(vid)
            if db_vendor is not None:
                manufacturer = db_vendor
            db_product = get_product(vid, pid)
            if db_product is not None:
                product = db_product

        print(f'USB {name: <4} [{vid:04x}:{pid:04x}] {manufacturer or "Unknown"} {product or "Unknown"}{serial}')

        if portinfo:
            speed = sysfs_float(port, "speed")
            power = sysfs_str(port, "bMaxPower")
            rx_lanes = sysfs_int(port, "rx_lanes")
            tx_lanes = sysfs_int(port, "tx_lanes")
            if speed > 10:
                speed = int(speed)
            if speed < 1000:
                speed = f"{speed} Mbps"
            else:
                speed = f"{speed / 1000} Gbps {rx_lanes}x{tx_lanes}"
            print(f"   Speed: {speed}, MaxPower: {power}")

        if intfinfo:
            device_class = sysfs_hex(port, 'bDeviceClass')
            device_subclass = sysfs_hex(port, 'bDeviceSubClass')
            device_protocol = sysfs_hex(port, 'bDeviceProtocol')
            print(f"   Class {device_class:02X} SubClass {device_subclass:02X} Protocol {device_protocol:02X}")
            for intf in glob.glob(os.path.join(port, "*:*")):
                number = sysfs_int(intf, "bInterfaceNumber")
                intf_class = sysfs_hex(intf, "bInterfaceClass")
                intf_subclass = sysfs_hex(intf, "bInterfaceSubClass")
                intf_protocol = sysfs_hex(intf, "bInterfaceProtocol")
                intf_name = sysfs_str(intf, "interface")
                intf_description = f"{intf_class:02X}/{intf_subclass:02X}/{intf_protocol:02X}"
                print(f"      Interface {number} {intf_description} {intf_name or 'Unknown'}")
        if devinfo:
            for intf in glob.glob(os.path.join(port, "*:*")):

                # Check for disks
                for scsi in glob.glob(os.path.join(intf, "host*/target*/*:*/block/*")):
                    devname = os.path.basename(scsi)
                    print(f"   Device /dev/{devname}")

                # Check for mmc storage
                for mmc in glob.glob(os.path.join(intf, "*/mmc_host/*")):
                    devname = os.path.basename(mmc)
                    mmcnum = devname.replace('mmc', '')
                    print(f"   Device /dev/mmcblk{mmcnum}")

                # Check for serial ports
                for device in glob.glob(os.path.join(intf, "tty*")):
                    ttydir = os.path.basename(device)
                    if ttydir == "tty":
                        device = list(glob.glob(os.path.join(device, '*')))[0]
                        ttydir = os.path.basename(device)
                    print(f"   Device /dev/{ttydir}")

                # Check for usbmisc
                for device in glob.glob(os.path.join(intf, "usbmisc/*")):
                    devname = os.path.basename(device)
                    print(f"   Device /dev/usb/{devname}")

                # Check for v4l2
                for device in glob.glob(os.path.join(intf, "video4linux/video*")):
                    devname = os.path.basename(device)
                    print(f"   Device /dev/{devname}")
                for device in glob.glob(os.path.join(intf, "media*")):
                    devname = os.path.basename(device)
                    print(f"   Device /dev/{devname}")

                # Check for input devices
                for device in glob.glob(os.path.join(intf, "input/input*/event*")):
                    devname = os.path.basename(device)
                    print(f"   Device /dev/input/{devname}")

                # Some input drivers have deeper nested paths
                for device in glob.glob(os.path.join(intf, "*/input/input*/event*")):
                    devname = os.path.basename(device)
                    print(f"   Device /dev/input/{devname}")

                # Check for network devices
                for device in glob.glob(os.path.join(intf, "net/*")):
                    devname = os.path.basename(device)
                    print(f"   Device {devname}")


def main():
    parser = argparse.ArgumentParser(description="USB listing tool")
    parser.add_argument('filter', help="Filter on port numbers", nargs="*")
    parser.add_argument('--no-db', '-n', action='store_true', help="Don't use the hardware database for names",
                        dest='nodb')
    parser.add_argument('--no-fixed', '-r', action='store_true', help="Don't show non-removable usb devices",
                        dest='nofixed')
    parser.add_argument('--portinfo', '-p', action='store_true', help="Show detailed port data")
    parser.add_argument('--devinfo', '-d', action='store_true', help="Show detailed kernel device info")
    parser.add_argument('--interfaces', '-i', action='store_true', help="Show detailed interface info")
    args = parser.parse_args()

    if len(args.filter) == 1 and args.filter[0].lower().startswith("select"):
        query.init()
        query.query(args.filter[0])
    else:
        get_ports(use_db=not args.nodb, fixed=not args.nofixed, portinfo=args.portinfo, devinfo=args.devinfo,
                  intfinfo=args.interfaces, filter=args.filter)


if __name__ == '__main__':
    main()
