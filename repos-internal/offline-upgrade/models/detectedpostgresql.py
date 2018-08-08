from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


class DetectedPostgreSql(Model):
    topic = SystemInfoTopic
    version = fields.String(required=True)
    data_path = fields.String(required=True)
