from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


class DetectedPython2Scripts(Model):
    topic = SystemInfoTopic
    scripts = fields.List(fields.String(), required=True, default=[])
