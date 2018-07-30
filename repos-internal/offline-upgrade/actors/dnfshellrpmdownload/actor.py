from tempfile import NamedTemporaryFile
from subprocess import check_call

from leapp.actors import Actor
from leapp.tags import DownloadPhaseTag, IPUWorkflowTag


class DNFShellRPMDownload(Actor):
    name = 'dnf_shell_rpm_download'
    description = 'No description has been provided for the dnf_shell_rpm_download actor.'
    consumes = ()
    produces = ()
    tags = (DownloadPhaseTag, IPUWorkflowTag)

    def process(self):
        with NamedTemporaryFile() as script:
            script.write('\n'.join([
                'distro-sync --downloadonly'
            ]))
            script.flush()
            check_call([
                '/usr/bin/dnf',
                'shell',
                '-y',
                '--releasever', '29',
                '--allowerasing',
                '--nogpgcheck',
                '--downloadonly',  # Needed here to avoid some weird behavior
                script.name
            ])
