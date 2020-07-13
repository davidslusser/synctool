from django.db import models
from jsonfield import JSONField

# import third party modules
from auditlog.registry import auditlog
from djangohelpers.managers import HandyHelperModelManager


class SyncManagerBase(models.Model):
    """ abstract model for common syncmgr db fields """
    objects = HandyHelperModelManager()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="date/time when this row was added")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="date/time when this row was updated")
    active = models.BooleanField(default=True, help_text="select if this record is currently active")

    class Meta:
        abstract = True
        ordering = ('-created_at', )


class AuthenticationType(SyncManagerBase):
    """ table of types of credentials """
    name = models.CharField(max_length=16, help_text='type of credential')
    description = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class SyncEventStatus(SyncManagerBase):
    """ table of types of statuses for a SyncEvent """
    name = models.CharField(max_length=16, help_text='name of status')
    description = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class SyncEventResult(SyncManagerBase):
    """ table of types of results for a SyncEvent """
    name = models.CharField(max_length=16, help_text='name of result')
    description = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class Service(SyncManagerBase):
    """ table of services with API endpoints that can be synced from/to """
    name = models.CharField(max_length=32, unique=True, help_text='name of service')
    auth_type = models.ForeignKey(AuthenticationType, on_delete=models.CASCADE)
    uid = models.CharField(max_length=32, blank=True, null=True, help_text='')
    pwd = models.CharField(max_length=32, blank=True, null=True,  help_text='')
    token = models.CharField(max_length=64, blank=True, null=True,  help_text='')

    def __str__(self):
        return self.name


class FieldMapEntry(SyncManagerBase):
    """ table of fields to sync from/to """
    src_field = models.CharField(max_length=32, help_text='')
    dst_field = models.CharField(max_length=32, help_text='')
    src_regex = models.CharField(max_length=32, blank=True, null=True, help_text='')
    dst_regex = models.CharField(max_length=32, blank=True, null=True,  help_text='')
    search_field = models.BooleanField(default=False,
                                       help_text='Marks this field as a \'search field.\' When syncing, a GET request '
                                                 'will first check for an existing entry using search fields. '
                                                 'If found, other fields will be updated with a PATCH request. '
                                                 'Fields should be marked as a \'search field\' if their value is not '
                                                 'expected to change. If no \'search fields\' are available, new '
                                                 'entries will be created in the destination service, which could lead '
                                                 'to duplicates.'
                                       )


class SyncSchedule(SyncManagerBase):
    """ schedule to run a SyncEntry on """
    cron = models.CharField(max_length=16, help_text='schedule, in cron format, this sync entry should run')
    description = models.CharField(max_length=32, blank=True, null=True, help_text='detail this cron schedule')

    def __str__(self):
        return self.cron


class SyncEntry(SyncManagerBase):
    """ table of things to sync from/to """
    owner = models.CharField(max_length=128)
    src = models.ForeignKey(Service, related_name='src_sync_entry', on_delete=models.CASCADE)
    dst = models.ForeignKey(Service, related_name='dst_sync_entry', on_delete=models.CASCADE)
    src_endpoint = models.URLField()
    dst_endpoint = models.URLField()
    src_schema = JSONField()
    dst_schema = JSONField()
    dst_detail_field = models.CharField(max_length=32, default='id',
                                        help_text='Name of field used for the detail URL. This is usually \'id\' but'
                                                  'could be something else like a UUID or name.')
    schedule = models.ForeignKey(SyncSchedule, blank=True, null=True ,on_delete=models.CASCADE)
    field_map = models.ManyToManyField(FieldMapEntry, blank=True, null=True)


class SyncEvent(SyncManagerBase):
    """ table recording sync requests """
    sync_entry = models.ForeignKey(SyncEntry, on_delete=models.CASCADE)
    status = models.ForeignKey(SyncEventStatus, null=True, on_delete=models.SET_NULL)
    result = models.ForeignKey(SyncEventResult, null=True, on_delete=models.SET_NULL)
    output = models.TextField(blank=True, null=True)


# Models to register with AuditLog
auditlog.register(AuthenticationType)
auditlog.register(Service)
auditlog.register(FieldMapEntry)
auditlog.register(SyncSchedule)
auditlog.register(SyncEntry)
