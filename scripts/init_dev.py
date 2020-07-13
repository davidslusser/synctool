#!/usr/bin/env python

# import system modules
import sys
import os
import datetime
import argparse
import string
import random
import logging
import environ
import django
from django.db.models import signals

# setup django
sys.path.append(str(environ.Path(__file__) - 2))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'synctool.settings')
django.setup()

__version__ = '0.0.1'

# import models
from syncmgr.models import (AuthenticationType, SyncEventStatus, SyncEventResult, Service,
                            FieldMapEntry, SyncSchedule, SyncEntry, SyncEvent)

from demo_app.models import (PersonOne, PersonTwo, CabinetOne, CabinetTwo)


def get_opts():
    """ Return an argparse object. """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--verbose', default=logging.INFO, action='store_const',
                        const=logging.DEBUG, help='enable debug logging')
    parser.add_argument('--version', action='version', version=__version__, help='show version and exit')
    parser.add_argument('--clean', action='store_true', required=False, help='delete existing records first')
    parser.add_argument('--disable_signals', action='store_true', required=False, help='disable django signals')
    args = parser.parse_args()
    logging.basicConfig(level=args.verbose)
    return args


def disconnect_signals():
    """ disable signals while running this script """
    logging.info('disabling signals')
    pass


def clean_syncmgr():
    """ delete all exiting records before generating new local dev data """
    logging.info('deleting syncmgr data')
    AuthenticationType.objects.all().delete()
    SyncEventStatus.objects.all().delete()
    SyncEventResult.objects.all().delete()
    Service.objects.all().delete()
    FieldMapEntry.objects.all().delete()
    SyncSchedule.objects.all().delete()
    SyncEntry.objects.all().delete()
    SyncEvent.objects.all().delete()


def clean_demo_app():
    """ delete records from demo_app """
    logging.info('deleting demo_app data')
    PersonOne.objects.all().delete()
    CabinetOne.objects.all().delete()


def clean():
    """ clean all """
    clean_demo_app()
    clean_syncmgr()


def get_random_alpha_numeric_string(length=8, include_digits=True):
    """ create a string of random characters """
    characters = string.ascii_letters
    if include_digits:
        characters += string.digits
    return ''.join((random.choice(characters) for i in range(length)))


def create_authentication_types():
    """ create some AuthenticationType entries """
    logging.info('Creating AuthenticationType entries')
    entry_list = [
        {'name': 'none', 'description': 'no authentication required'},
        {'name': 'user', 'description': 'user and password'},
        {'name': 'token', 'description': 'token based authentication'},
    ]
    for i in entry_list:
        AuthenticationType.objects.get_or_create(**i, defaults=i)


def create_sync_event_statuses():
    """ create some SyncEventStatus entries """
    logging.info('Creating SyncEventStatus entries')
    entry_list = [
        {'name': 'created', 'description': 'This sync event has been created, but work has not begun'},
        {'name': 'in progress', 'description': 'work on this sync event has started'},
        {'name': 'completed', 'description': 'sync event has been completed'},
        {'name': 'unknown', 'description': 'This sync event is in an unknown status; an error has likely occurred'},
    ]
    for i in entry_list:
        SyncEventStatus.objects.get_or_create(**i, defaults=i)


def create_sync_event_results():
    """ create some SyncEventResult entries """
    logging.info('Creating SyncEventResult entries')
    entry_list = [
        {'name': 'success', 'description': 'this sync event has completed successfully'},
        {'name': 'fail', 'description': 'this sync event failed to complete'},
        {'name': 'error', 'description': 'an error occurred when attempting to complete this sync event'},
        {'name': 'unknown', 'description': 'the result of this sync event is unknown; the sync event is '
                                           'either incomplete or an error has occurred'},
    ]
    for i in entry_list:
        SyncEventResult.objects.get_or_create(name=i['name'], defaults=i)


def create_sync_schedules():
    """ create some SyncSchedule entries """
    logging.info('Creating SyncSchedule entries')
    entry_list = [
        {'cron': '*/30 0 * * * ', 'description': 'run every 30 minutes'},
        {'cron': '* */6 * * * ', 'description': 'run every 6 hours'},
        {'cron': '* /1 * * *', 'description': 'run every hour'},
        {'cron': '* * */1 * * ', 'description': 'run every day'},
        {'cron': '* * * */1 * ', 'description': 'run every month'},
    ]
    for i in entry_list:
        SyncSchedule.objects.get_or_create(**i, defaults=i)


def add_demo_app_service():
    """ """
    logging.info('Adding demo_app as a service')
    service_name = 'demo_app'
    data = {
        'name': service_name,
        'auth_type': AuthenticationType.objects.get_object_or_none(name='none'),
        'uid': get_random_alpha_numeric_string(8),
        'pwd': get_random_alpha_numeric_string(8),
        'token': None,
    }
    Service.objects.get_or_create(name=service_name, defaults=data)


def create_services():
    """ create some Service entries """
    logging.info('Creating Service entries')
    name_list = ['service_01', 'service_02', 'service_03', 'service_04', 'service_05']
    for name in name_list:
        uid = None
        pwd = None
        token = None
        auth_type = AuthenticationType.objects.get_random_row()
        if auth_type.name == 'token':
            token = get_random_alpha_numeric_string(16)
        elif auth_type.name == 'user':
            uid = get_random_alpha_numeric_string(8)
            pwd = get_random_alpha_numeric_string(8)
        data = {
            'name': name,
            'auth_type': auth_type,
            # 'uid': uid,
            # 'pwd': pwd,
            # 'token': token,
        }
        Service.objects.get_or_create(name=name, defaults=data)


# def create_sync_entries():
#     """ create some SyncEntry entries """
#     logging.info('Creating SyncEntry entries')
#     owner_list = ['owner_01', 'owner_02', 'owner_03', 'owner_04', 'owner_05']
#     for i in range(3):
#         src = Service.objects.get_random_row()
#         dst = Service.objects.get_random_row()
#         data = {
#             'owner': random.choice(owner_list),
#             'src': src,
#             'dst': dst,
#             'src_endpoint': 'https://{}.net/api/{}'.format(src, get_random_alpha_numeric_string()),
#             'dst_endpoint': 'https://{}.net/api/{}'.format(dst, get_random_alpha_numeric_string()),
#             'src_schema': '{}',
#             'dst_schema': '{}',
#             'schedule': SyncSchedule.objects.get_random_row(),
#         }
#         obj, is_new = SyncEntry.objects.get_or_create(**data, defaults=data)
#         if is_new:
#             pass

def add_demo_app_sync_entries():
    """ add some SyncEntry for demo_app """
    logging.info('Adding SyncEntry entries for demo_app')
    # add PersonOne to PersonTwo sync
    owner_list = ['owner_01', 'owner_02', 'owner_03', 'owner_04', 'owner_05']
    data = {
    'owner': random.choice(owner_list),
    'src': Service.objects.get(name='demo_app'),
    'dst': Service.objects.get(name='demo_app'),
    'src_endpoint': 'http://127.0.0.1:8000/demo_app/personone/',
    'dst_endpoint': 'http://127.0.0.1:8000/demo_app/persontwo/',
    'src_schema': '{}',
    'dst_schema': '{}',
    'schedule': SyncSchedule.objects.get_random_row(),
    }
    obj, is_new = SyncEntry.objects.get_or_create(**data, defaults=data)
    if is_new:
        pass

    # add CabinetOne to CabinetTwo sync


def create_sync_entries():
    """ create some SyncEntry entries """
    logging.info('Creating SyncEntry entries for demo')
    owner_list = ['owner_01', 'owner_02', 'owner_03', 'owner_04', 'owner_05']
    for i in range(3):
        src = Service.objects.get_random_row()
        dst = Service.objects.get_random_row()
        data = {
            'owner': random.choice(owner_list),
            'src': src,
            'dst': dst,
            'src_endpoint': 'https://{}.net/api/{}'.format(src, get_random_alpha_numeric_string()),
            'dst_endpoint': 'https://{}.net/api/{}'.format(dst, get_random_alpha_numeric_string()),
            'src_schema': '{}',
            'dst_schema': '{}',
            'schedule': SyncSchedule.objects.get_random_row(),
        }
        obj, is_new = SyncEntry.objects.get_or_create(**data, defaults=data)
        if is_new:
            pass


def create_person_one():
    """ create PersonOne entries """
    logging.info('Creating PersonOne entries')
    entry_list = [
        {'first_name': 'Matt', 'last_name': 'Merdock', 'phone_number': '101-222-3333'},
        {'first_name': 'Jessica', 'last_name': 'Jones', 'phone_number': '202-333-4444'},
        {'first_name': 'Luke', 'last_name': 'Cage', 'phone_number': '303-444-5555'},
        {'first_name': 'Danny', 'last_name': 'Rand', 'phone_number': '404-555-6666'},

    ]
    for i in entry_list:
        PersonOne.objects.get_or_create(**i, defaults=i)


def create_cabinet_one():
    """ create CabinetOne entries """
    logging.info('Creating CabinetOne entries')
    entry_list = [
        {'name': 'cab_101', 'location': 'cage_1000'},
        {'name': 'cab_102', 'location': 'cage_1000'},
        {'name': 'cab_201', 'location': 'cage_2000'},
        {'name': 'cab_202', 'location': 'cage_2000'},

    ]
    for i in entry_list:
        CabinetOne.objects.get_or_create(**i, defaults=i)


def create_syncmgr_entries():
    """ create all the syncmgr things """
    create_authentication_types()
    create_sync_event_statuses()
    create_sync_event_results()
    create_sync_schedules()
    create_services()
    add_demo_app_service()
    create_sync_entries()


def create_demo_app_entries():
    """ create all the demo_app entries """
    create_person_one()
    create_cabinet_one()


def create_all():
    """ create all the things """
    create_syncmgr_entries()
    create_demo_app_entries()


def main():
    """ script entry point """
    opts = get_opts()
    logging.info('Starting script')
    if opts.disable_signals:
        disconnect_signals()

    if opts.clean:
        clean()

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now() - start_time

    create_all()

    logging.info('')
    logging.info('Script completed in: {}'.format(end_time))


if __name__ == '__main__':
    sys.exit(main())
