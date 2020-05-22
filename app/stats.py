import collections
from launchpadlib.launchpad import Launchpad
from pprint import pprint
import os


_lp_cachedir = os.path.expanduser("~/.launchpadlib/cache/")
launchpad = Launchpad.login_anonymously('anon', 'production', _lp_cachedir)


def get_binaries(ppa_owner, ppa_name, package):
    owner = launchpad.people[ppa_owner]
    ppa = owner.getPPAByName(name=ppa_name)

    binaries = ppa.getPublishedBinaries(binary_name=package)

    # Remove binaries which are copied.
    def is_not_copy(binary):
        return binary.copied_from_archive_link is None
    binaries = filter(is_not_copy, binaries)

    return binaries

def get_binary_info(binary):
    daily_downloads = binary.getDownloadCounts()
    daily = collections.defaultdict(lambda: 0)
    for downloads in daily_downloads:
        daily[downloads.day] += downloads.count

    info = {
        'display_name': binary.display_name,
        'version': binary.binary_package_version,
        #'architecture_specific': binary.architecture_specific,
        'distro_arch_series_link': binary.distro_arch_series_link,
        'total_downloads': binary.getDownloadCount(),
        'daily_downloads': daily,
        'binary': binary,
    }
    return info

if __name__ == '__main__':
    binaries = get_binaries('hsheth2', 'ppa', 'cava')
    for binary in binaries:
        info = get_binary_info(binary)
        pprint(info)
        break
