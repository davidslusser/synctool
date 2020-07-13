import logging
import re
import requests

# import models
from syncmgr.models import (SyncEntry, SyncEvent)


def build_data(sync_entry, src_entry_data, action='get'):
    """
    Build data to get/post/patch to destination; including regex conversion

    Args:
        action: api action to build data for (get/patch/search)
        sync_entry: SyncEntry object
        src_entry_data: data entry as received from the source endpoint

    Returns:
        dictionary of data to use in the get/post/patch call to the destination endpoint
    """
    data = {}
    if action == 'get':
        queryset = sync_entry.field_map.filter(active=True)
    elif action == 'patch':
        queryset = sync_entry.field_map.filter(active=True, search_field=False)
    elif action == 'search':
        queryset = sync_entry.field_map.filter(active=True, search_field=True)
    else:
        return data

    for field_map in queryset:
        if field_map.src_regex and field_map.dst_field:
            data[field_map.dst_field] = re.sub(r'(\d{3})-(\d{3})-(\d{4})',
                                               r'(\1) \2-\3',
                                               src_entry_data[field_map.src_field])
        else:
            data[field_map.dst_field] = src_entry_data[field_map.src_field]
    return data


def get_results(schema, resp):
    """
    Get data for from a python requests response. Uses json schema to determine if response data is paginated.

    Args:
        schema: json schema as defined in the SyncEntry
        resp: response from python requests call

    Returns:
        list of results from the API
    """

    # determine if results are paginated
    if schema['type'] == 'object':
        return resp.json()['results']
    else:
        return resp.json()


def run_sync():
    """ execute sync on all active SyncEntry objects """
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

            # get data from destination
            dst_get_resp = get_results(schema=sync_entry.dst_schema,
                                       resp=requests.get(url=sync_entry.dst_endpoint,
                                                         params=build_data(sync_entry, result, action='search')),
                                       )

            # if entry is not in destination, POST to destination
            if not dst_get_resp.json()['results']:
                logging.info('data not in destination; {}, posting now...')
                dst_post_resp = requests.post(sync_entry.dst_endpoint,
                                              data=data,
                                              headers={'Authorization': 'token {}'.format(sync_entry.dst.token)},
                                              )

            # if entry is in destination, PATCH to destination
            else:
                logging.info('data is in destination; {}, patching now...')
                dst_patch_resp = requests.patch('{}{}/'.format(sync_entry.dst_endpoint,
                                                               dst_get_resp[sync_entry.dst_detail_field]),
                                                data=build_data(sync_entry, result, action='patch'),
                                                headers={'Authorization': 'token {}'.format(sync_entry.dst.token)},
                                                )
