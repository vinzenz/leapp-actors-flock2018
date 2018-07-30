from tempfile import NamedTemporaryFile
from subprocess import check_call

from leapp.actors import Actor
from leapp.tags import RPMUpgradePhaseTag, IPUWorkflowTag


class DnfShellRpmUpgrade(Actor):
    name = 'dnf_shell_rpm_upgrade'
    description = 'No description has been provided for the dnf_shell_rpm_upgrade actor.'
    consumes = ()
    produces = ()
    tags = (RPMUpgradePhaseTag, IPUWorkflowTag)

    def process(self):
        with NamedTemporaryFile() as script:
            script.write('\n'.join([
                'distro-sync'
            ]).encode('utf-8'))
            script.flush()
            check_call([
                '/usr/bin/dnf',
                'shell',
                '-y',
                '-C',
                '--repofrompath',
                'leapprepo,https://copr-be.cloud.fedoraproject.org/results/evilissimo/leapp-flock2018/fedora-rawhide-x86_64/',
                '--releasever', '29',
                '--allowerasing',
                '--nogpgcheck',
                script.name
            ])
