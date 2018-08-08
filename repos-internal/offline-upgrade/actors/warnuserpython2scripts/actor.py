from leapp.actors import Actor
from leapp.models import DetectedPython2Scripts
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag
from leapp.dialogs import Dialog, BooleanComponent

class WarnUserPython2Scripts(Actor):
    name = 'warn_user_python2_scripts'
    description = 'No description has been provided for the warn_user_python2_scripts actor.'
    consumes = (DetectedPython2Scripts,)
    produces = ()
    tags = (ChecksPhaseTag, IPUWorkflowTag)
    dialogs = (
        Dialog(
            scope='warn_python2_user_scripts',
            title='Warning Python 2.x scripts detected',
            reason='''
Python 2.x has been depreated and it is no longer supported by Fedora.
You have the option to review the list of scripts that potentially will
no longer work with the python3 installation.'''.strip(),
            components=(
            BooleanComponent(
                key='display',
                default=False,
                label='Would you like to display the affected scripts?'),)),
        Dialog(
            scope='continue_warn_python2_user_scripts',
            title='',
            reason='',
            components=(
                BooleanComponent(
                    key='continue',
                    default=True,
                    label='Continue with upgrade?'),)))

    def process(self):
        scripts = list(self.consume(DetectedPython2Scripts))
        if scripts and self.request_answers(self.dialogs[0]).get('display', False):
            all_scripts = set()
            for message in scripts:
                all_scripts.update(message.scripts)
            print('- ' + '\n- '.join(all_scripts), '\n')
            if not self.request_answers(self.dialogs[1]).get('continue', False):
                self.report_error('User requested abortion')
