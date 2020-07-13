#!/usr/bin/env python

# import system modules
import sys
import os
import datetime
import argparse
import string
import random
import re
import requests
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
    parser.add_argument('--disable_signals', action='store_true', required=False, help='disable django signals')
    args = parser.parse_args()
    logging.basicConfig(level=args.verbose)
    return args


def disconnect_signals():
    """ disable signals while running this script """
    logging.info('disabling signals')
    pass


def build_data(sync_entry, src__entry_data):
    """ build data to get/post/patch to destination; including regex conversion """
    data = {}
    for field_map in sync_entry.field_map.filter(active=True):
        if field_map.src_regex and field_map.dst_field:
            data[field_map.dst_field] = re.sub(r'(\d{3})-(\d{3})-(\d{4})',
                                               r'(\1) \2-\3',
                                               src__entry_data[field_map.src_field])
        else:
            data[field_map.dst_field] = src__entry_data[field_map.src_field]
    return data


def build_search_data(sync_entry, src__entry_data):
    """ build data to get/post/patch to destination; including regex conversion """
    data = {}
    for field_map in sync_entry.field_map.filter(active=True, search_field=True):
        if field_map.src_regex and field_map.dst_field:
            data[field_map.dst_field] = re.sub(r'(\d{3})-(\d{3})-(\d{4})',
                                               r'(\1) \2-\3',
                                               src__entry_data[field_map.src_field])
        else:
            data[field_map.dst_field] = src__entry_data[field_map.src_field]
    return data


def build_patch_data(sync_entry, src__entry_data):
    """ build data to get/post/patch to destination; including regex conversion """
    data = {}
    for field_map in sync_entry.field_map.filter(active=True, search_field=False):
        if field_map.src_regex and field_map.dst_field:
            data[field_map.dst_field] = re.sub(r'(\d{3})-(\d{3})-(\d{4})',
                                               r'(\1) \2-\3',
                                               src__entry_data[field_map.src_field])
        else:
            data[field_map.dst_field] = src__entry_data[field_map.src_field]
    return data


def sync_all():
    """ sync all the things

    params == search data
    data   == data to be entered
    """
    # get SyncEntry entries
    sync_entries = SyncEntry.objects.filter(active=True)
    for sync_entry in sync_entries:
        logging.info('syncing {}:{} to {}:{}'.format(sync_entry.src,
                                                     sync_entry.src_endpoint.rstrip('/').split('/')[-1],
                                                     sync_entry.dst,
                                                     sync_entry.dst_endpoint.rstrip('/').split('/')[-1]
                                                     ))

        # first get data from the source to see if we need to POST, PATCH, or skip (if destination entry is current)
        src_resp = requests.get(sync_entry.src_endpoint)

        # determine if results are paginated
        if sync_entry.src_schema['type'] == 'object':
            src_lookup = src_resp.json()['results']
        else:
            src_lookup = src_resp.json()

        # iterate through all results and build params
        for result in src_lookup:

            # build data to get/post/patch to destination
            data = build_data(sync_entry, result)

            # if there are no search_fields identified in the field_map, skip update and POST to destination
            if not sync_entry.field_map.filter(active=True, search_field=True):
                logging.info('no search fields identified, adding new entry in destination')
                dst_post_resp = requests.post(sync_entry.dst_endpoint,
                                              data=data,
                                              headers={'Authorization': 'token {}'.format(sync_entry.dst.token)},
                                              )

            # if there are search fields, first do a GET from the destination, then do a PATCH to the destination
            # using the non-search fields if data from source do not match data in the destination

            # get data from dst
            dst_get_resp = requests.get(sync_entry.dst_endpoint, params=build_search_data(sync_entry, result))

            # if entry is not in destination, POST to destination
            print(dst_get_resp.json()['results'][0])
            if not dst_get_resp.json()['results']:
                logging.info('data not in destination; {}, posting now...')
                dst_post_resp = requests.post(sync_entry.dst_endpoint,
                                              data=data,
                                              headers={'Authorization': 'token {}'.format(sync_entry.dst.token)},
                                              )

            # if entry is in destination, PATCH to destination
            logging.info('data is in destination; {}, patching now...')
            dst_patch_resp = requests.patch('{}{}/'.format(sync_entry.dst_endpoint,
                                                           dst_get_resp.json()['results'][0][sync_entry.dst_detail_field]),
                                            data=build_patch_data(sync_entry, result),
                                            headers={'Authorization': 'token {}'.format(sync_entry.dst.token)},
                                            )
            print("TEST: ", dst_patch_resp)
            print("TEST: ", dst_patch_resp.url)


def main():
    """ script entry point """
    opts = get_opts()
    logging.info('Starting script')
    if opts.disable_signals:
        disconnect_signals()

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now() - start_time

    sync_all()

    logging.info('')
    logging.info('Script completed in: {}'.format(end_time))


if __name__ == '__main__':
    sys.exit(main())
