from leapp.actors import Actor
from leapp.models import DetectedPostgreSql
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag
from leapp.dialogs import Dialog, ChoiceComponent


_AVAILABLE_CHOICES = ('Switch to 9.x stream', 'Upgrade to latest', 'Abort upgrade')
_DIALOG_REASON = '''
We detected PostgreSQL version 9.x on your system.  The new version of Fedora
gives you the opportunity to switch to a PostgeSQL 9.x module stream. An
alternative choice you have, is to upgrade your PostgreSQL installation to
the latest version.
'''


_DIALOGS = (
    Dialog(scope='postgresql_module_switch',
           title='PostgreSQL 9.X module stream',
           reason=_DIALOG_REASON.strip(),
           components=(
               ChoiceComponent(
               key='switch',
               choices=_AVAILABLE_CHOICES,
               default=_AVAILABLE_CHOICES[1],
               label='How would you like to continue'),)),)


class SuggestModulePostgreSql(Actor):
    name = 'suggest_module_postgre_sql'
    description = 'No description has been provided for the suggest_module_postgre_sql actor.'
    consumes = (DetectedPostgreSql,)
    produces = ()
    tags = (ChecksPhaseTag, IPUWorkflowTag)
    dialogs = _DIALOGS

    def process(self):
        for detection in self.consume(DetectedPostgreSql):
            if detection.version.startswith('9'):
                self.log.info("Found version 9.x")
                result = self.request_answers(self.dialogs[0]).get('switch')
                if _AVAILABLE_CHOICES.index(result) == 2:
                    self.report_error('User requested abortion')
                
