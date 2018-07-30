from leapp.models import Model, fields
from leapp.topics import SystemInfoTopic

class PesRelease(Model):
    topic = SystemInfoTopic

    tag = fields.String(allow_null=True)
    os_name = fields.String(allow_null=True)
    major_version = fields.Integer()
    minor_version = fields.Integer()
    z_stream = fields.String(allow_null=True)


class PesPackage(Model):
    topic = SystemInfoTopic

    name = fields.String(allow_null=True)


class PesPackageSet(Model):
    topic = SystemInfoTopic

    set_id = fields.Integer()
    repository = fields.String(allow_null=True)
    package = fields.List(fields.Nested(PesPackage), default=[])


class PesAuthorProfile(Model):
    topic = SystemInfoTopic

    default_repository = fields.String(allow_null=True)
    default_release = fields.String(allow_null=True)
    follows = fields.List(fields.String(), default=[])


class PesAuthor(Model):
    topic = SystemInfoTopic

    id = fields.Integer()
    username = fields.String(allow_null=True)
    email = fields.String(allow_null=True)
    first_name = fields.String(allow_null=True)
    last_name = fields.String(allow_null=True)
    profile = fields.Nested(PesAuthorProfile)


class PesEvent(Model):
    topic = SystemInfoTopic

    id = fields.Integer()
    summary = fields.String(allow_null=True)
    docstring = fields.String(allow_null=True)
    action = fields.StringEnum(choices=['Present',
                                        'Removed',
                                        'Deprecated',
                                        'Replaced',
                                        'Split',
                                        'Merged',
                                        'Moved',
                                        'Renamed'])
    release = fields.Nested(PesRelease, default=None, allow_null=True)
    in_packageset = fields.Nested(PesPackageSet)
    out_packageset = fields.Nested(PesPackageSet, allow_null=True)
    author_id = fields.Nested(PesAuthor)
    created = fields.String(allow_null=True)
    links = fields.List(fields.String(), default=[])


class PesEventsList(Model):
    topic = SystemInfoTopic

    events = fields.List(fields.Nested(PesEvent), default=[])
