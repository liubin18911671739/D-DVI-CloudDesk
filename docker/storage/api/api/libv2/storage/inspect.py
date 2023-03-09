

import sys

import guestfs


def inspect_disk(path):
    g = guestfs.GuestFS(python_return_dict=True)
    g.add_drive_opts(path, readonly=1)
    g.launch()
    roots = g.inspect_os()
    disks = {"devices": roots}
    for root in roots:
        disks[root] = {
            "product_name": "%s" % (g.inspect_get_product_name(root)),
            "version": "%d.%d"
            % (g.inspect_get_major_version(root), g.inspect_get_minor_version(root)),
            "type": "%s" % (g.inspect_get_type(root)),
            "distro": "%s" % (g.inspect_get_distro(root)),
        }
    g.umount_all()
    return disks
