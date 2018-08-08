from leapp.actors import Actor
from leapp.tags import IPUWorkflowTag, ChecksPhaseTag
from leapp.models import DetectedPython2Scripts
from subprocess import check_output, call
import os

_EXCLUSION_PREFIXES = set([
    '/usr/lib/python3',
    '/usr/lib64/python3'
])

_FNULL = open(os.devnull, 'w')

def resolve(path):
    path = os.path.realpath(path)
    for prefix in _EXCLUSION_PREFIXES:
        if path.startswith(prefix):
            return ''
    return path


class ScanForPythonIncompatibleScripts(Actor):
    name = 'scan_for_python_incompatible_scripts'
    description = 'No description has been provided for the scan_for_python_incompatible_scripts actor.'
    consumes = ()
    produces = (DetectedPython2Scripts,)
    tags = (IPUWorkflowTag, ChecksPhaseTag)

    @staticmethod
    def find_paths(*paths):
        result = set()
        for path in paths:
            lines = check_output(['find', path, '-name', '*.py'], stderr=_FNULL).decode('utf-8').splitlines()
            result.update([resolve(line) for line in lines])
        return result.difference([''])
    
    def process(self):
        result = self.find_paths(
            '/'
        )
        failed_scripts = []
        for script in result:
            if call(['python3', '-m', 'py_compile', script], stdout=_FNULL, stderr=_FNULL) != 0:
                failed_scripts.append(script)
        if failed_scripts:
            self.produce(DetectedPython2Scripts(scripts=failed_scripts))

