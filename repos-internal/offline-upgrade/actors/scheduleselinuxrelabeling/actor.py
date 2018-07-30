from leapp.actors import Actor
from leapp.tags import FinalizationPhaseTag, IPUWorkflowTag


class ScheduleSeLinuxRelabeling(Actor):
    name = 'schedule_se_linux_relabeling'
    description = 'No description has been provided for the schedule_se_linux_relabeling actor.'
    consumes = ()
    produces = ()
    tags = (FinalizationPhaseTag, IPUWorkflowTag)

    def process(self):
        with open('/.autorelabel', 'w'):
            pass
