from django.contrib import admin

# import models
from syncmgr.models import (AuthenticationType,
                            SyncEventStatus,
                            SyncEventResult,
                            Service,
                            FieldMapEntry,
                            SyncSchedule,
                            SyncEntry,
                            SyncEvent
                            )


class AuthenticationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['active']


class SyncEventStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['active']


class SyncEventResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['active']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'auth_type', 'uid', 'pwd', 'token']
    search_fields = ['name', 'uid', 'pwd', 'token']
    list_filter = ['active', 'auth_type']


class FieldMapEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'src_field', 'dst_field', 'src_regex', 'dst_regex', 'search_field']
    search_fields = ['src_field', 'dst_field', 'src_regex', 'dst_regex']
    list_filter = ['active', 'search_field']


class SyncScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'cron', 'description']
    search_fields = ['cron', 'description']
    list_filter = ['active']


class SyncEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'owner', 'src', 'dst', 'src_endpoint', 'dst_endpoint', 'src_schema', 'dst_schema', 'schedule']
    search_fields = ['owner', 'src_endpoint', 'dst_endpoint', 'src_schema', 'dst_schema']
    list_filter = ['active', 'src', 'dst', 'schedule']


class SyncEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'sync_entry', 'status', 'result', 'output']
    search_fields = ['output']
    list_filter = ['active', 'sync_entry', 'status', 'result']


# register models
admin.site.register(AuthenticationType, AuthenticationTypeAdmin)
admin.site.register(SyncEventStatus, SyncEventStatusAdmin)
admin.site.register(SyncEventResult, SyncEventResultAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(FieldMapEntry, FieldMapEntryAdmin)
admin.site.register(SyncSchedule, SyncScheduleAdmin)
admin.site.register(SyncEntry, SyncEntryAdmin)
admin.site.register(SyncEvent, SyncEventAdmin)
