from django.contrib import admin

# import models
from demo_app.models import (PersonOne,
                             PersonTwo,
                             CabinetOne,
                             CabinetTwo
                             )


class PersonOneAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_filter = []


class PersonTwoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'phone']
    search_fields = ['fname', 'lname', 'phone']
    list_filter = []


class CabinetOneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location']
    search_fields = ['name', 'location']
    list_filter = []


class CabinetTwoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cab_name', 'room']
    search_fields = ['cab_name', 'room']
    list_filter = []


# register models
admin.site.register(PersonOne, PersonOneAdmin)
admin.site.register(PersonTwo, PersonTwoAdmin)
admin.site.register(CabinetOne, CabinetOneAdmin)
admin.site.register(CabinetTwo, CabinetTwoAdmin)
