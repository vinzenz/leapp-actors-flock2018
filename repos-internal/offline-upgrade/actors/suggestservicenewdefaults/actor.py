from leapp.actors import Actor
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag
from leapp.dialogs import ChoiceComponent, Dialog

_CHOICES = (
    'Discard changes and apply defaults',
    'Merge new defaults and keep my changes',
    'Keep previous defaults'
)
class SuggestServiceNewDefaults(Actor):
    name = 'suggest_service_new_defaults'
    description = 'No description has been provided for the suggest_service_new_defaults actor.'
    consumes = ()
    produces = ()
    tags = (ChecksPhaseTag, IPUWorkflowTag)
    dialogs = (Dialog(
        scope='new_service_defaults_dialog',
        title='New service defaults',
        reason='''
In the new version of Fedora changes have been made to the service defaults
and we detected customizations to your service defaults. Please select one
of the following strategies to use for the upgrade.'''.strip(),
        components=(ChoiceComponent(
            key='strategy',
            label='Strategy to use',
            default=_CHOICES[1],
            choices=_CHOICES
        ),)
    ),)

    def process(self):
        self.request_answers(self.dialogs[0])
