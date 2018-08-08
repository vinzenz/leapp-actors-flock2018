from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic


class SwitchToBLS(Model):
    topic = SystemInfoTopic
    answer = fields.Boolean(default=False, required=True)
