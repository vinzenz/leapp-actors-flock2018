from leapp.actors import Actor
from leapp.tags import FinalizationPhaseTag, IPUWorkflowTag


class SeLinuxRelabeling(Actor):
    name = 'se_linux_relabeling'
    description = 'No description has been provided for the se_linux_relabeling actor.'
    consumes = ()
    produces = ()
    tags = (FinalizationPhaseTag, IPUWorkflowTag)

    def process(self):
        from subprocess import check_call
        check_call(['/sbin/restorecon', '-Rv', '/'])
