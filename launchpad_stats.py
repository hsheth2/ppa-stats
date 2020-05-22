# See https://api.launchpad.net/+apidoc/devel.html#binary_package_publishing_history
# See https://help.launchpad.net/API/launchpadlib

# https://gist.github.com/springmeyer/2778600
# https://gist.github.com/stefansundin/f9df6c5e0fd184c60709

# TODO: look at https://github.com/YokoZar/ppa-stats/blob/master/ppa-stats

from launchpadlib.launchpad import Launchpad
import os

USERNAME='hsheth2'
PPA='ppa'
PACKAGE='cava'

cachedir = os.environ['HOME'] + '/.launchpadlib/cache/'
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)

ppa = launchpad.people[USERNAME].getPPAByName(name=PPA)
bins = ppa.getPublishedBinaries(binary_name=PACKAGE)

for bin in bins:
    if bin.copied_from_archive_link is None:
        print(bin.binary_package_version, bin.getDownloadCount(), bin.architecture_specific, bin.display_name, bin)


