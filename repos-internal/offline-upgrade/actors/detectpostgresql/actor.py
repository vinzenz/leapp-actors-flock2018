from leapp.actors import Actor
from leapp.models import DetectedPostgreSql
from leapp.tags import FactsPhaseTag, IPUWorkflowTag


class DetectPostgreSql(Actor):
    name = 'detect_postgre_sql'
    description = 'No description has been provided for the detect_postgre_sql actor.'
    consumes = ()
    produces = (DetectedPostgreSql,)
    tags = (FactsPhaseTag, IPUWorkflowTag)

    def process(self):
        # Should actually detect PostgreSQL - For demo purposes this is only a static message
        detections = [
            DetectedPostgreSql(version='9.6', data_path='/var/lib/pgsql96'),
            DetectedPostgreSql(version='10.4', data_path='/var/lib/pgsql10')
        ]
        for detected in detections:
            self.log.info('[DISOVERY] Detected PostgreSQL {version} with data path = {data_path}'.format(**detected.dump()))
        self.produce(*detections)
