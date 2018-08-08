from leapp.actors import Actor
from leapp.models import DetectedPython2Scripts
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag
from leapp.dialogs import Dialog, ChoiceComponent


_AVAILABLE_CHOICES = ('Subscribe to the 2.7 stream', 'Do nothing', 'Abort upgrade')
_DIALOG_REASON = '''
We detected Python 2 scripts on your system. The new version of Fedora
gives you the opportunity to switch to the Python 2.7 module stream.
'''


class SuggestPython2Module(Actor):
    name = 'suggest_python2_module'
    description = 'No description has been provided for the suggest_python2_module actor.'
    consumes = (DetectedPython2Scripts,)
    produces = ()
    tags = (ChecksPhaseTag, IPUWorkflowTag)
    dialogs = (
        Dialog(
            scope='suggest_python2_module',
            title='Python 2.7 module stream',
            reason=_DIALOG_REASON.strip(),
            components=(
                ChoiceComponent(
                key='switch',
                choices=_AVAILABLE_CHOICES,
                default=_AVAILABLE_CHOICES[1],
                label='How would you like to continue'),)),)

    def process(self):
        if self.consume(DetectedPython2Scripts):
            result = self.request_answers(self.dialogs[0]).get('switch')
            if _AVAILABLE_CHOICES.index(result) == 2:
                self.report_error('User requested abortion')
