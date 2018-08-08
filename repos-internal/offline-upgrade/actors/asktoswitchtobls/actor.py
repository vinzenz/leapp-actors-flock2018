from leapp.actors import Actor
from leapp.tags import IPUWorkflowTag, FactsPhaseTag
from leapp.models import SwitchToBLS
from leapp.dialogs import Dialog, BooleanComponent

class AskToSwitchToBls(Actor):
    name = 'ask_to_switch_to_bls'
    description = 'No description has been provided for the ask_to_switch_to_bls actor.'
    consumes = ()
    produces = (SwitchToBLS,)
    tags = (IPUWorkflowTag, FactsPhaseTag)
    dialogs = (
        Dialog(scope='switch_to_bls', reason='''
The Boot Loader Specification (BLS) defines a scheme and file format to manage
boot loader configuration for each boot option in a drop-in directory, without
the need to manipulate bootloader configuration files. Directories of
individual drop-in configuration files are standard for many purposes on Linux
nowadays, so the goal is to also extend this concept for boot menu entries.'''.strip(),
               title='Convert to Boot Loader Specification?',
               components=(BooleanComponent(key='answer', default=False, label='Would you like to switch?'),)),)

    def process(self):
        if self.request_answers(self.dialogs[0]).get('answer', False):
            self.produce(SwitchToBLS(value=True))
