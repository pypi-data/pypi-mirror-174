from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.uniquedevices import *

job = {
    'name': 'S-UD-60to180',
    'version': '99.99.99',
    'input_stream_name': create_key_name(Type.STREAM.value, '1HOUR', Dimension.SECTION.value, '', '', Metric.UNIQUE_DEVICES.value),
    'dimension': Dimension.SECTION.value,
    'number_of_rotated_keys': 3, # rotate 3 keys of 1 hour each
    'write_to_ts': True,
    'timeseries_name': '3HOURS',
    # 'key_expire_duration_sc': 604940, # keep 56 keys -> merged key expire 7 days later
    'key_expire_duration_sc': 1209880, # TEST
    'batch_size': 9999999,
    'batch_interval_ms': 10800000, # run the job every 3 hours
    'output_stream_name': create_key_name(Type.STREAM.value, '3HOURS', Dimension.SECTION.value, '', '', Metric.UNIQUE_DEVICES.value)
}

# Todo: unregister_old_versions job
# unregister_old_versions(job.get('name'), job.get('version'))

tracker_log(f'Register {job.get("name")} ...')

desc_json = {
    "name": job.get('name'),
    "version": job.get('version'),
    "desc": f"Rotate Section Pageviews Keys, 1 hour to 3 hours buckets"
}

GB("StreamReader", desc=json.dumps(desc_json)). \
    aggregate([],
              lambda a, r: a + [r['value']],
              lambda a, r: a + r). \
    map(lambda record: transform(record, job.get('number_of_rotated_keys'), job.get('dimension'))). \
    foreach(lambda record: load_device(
        job.get('name'),
        record,
        job.get('dimension'),
        job.get('write_to_ts'),
        job.get('timeseries_name'),
        job.get('key_expire_duration_sc'),
        job.get('input_stream_name'),
        job.get('output_stream_name')
    )). \
    foreach(lambda records: tracker_log(f'ids:{len(records.get("ids"))} merged:{len(records.get("merge"))} reinjected:{len(records.get("reinject"))} - {records}', f'{job.get("name")} - ')). \
    register(
        prefix=job.get('input_stream_name'),
        convertToStr=True,
        collect=True,
        onFailedPolicy='abort',
        onFailedRetryInterval=1,
        batch=job.get('batch_size'),
        duration=job.get('batch_interval_ms'),
        trimStream=False)

tracker_log(f'Register {job.get("name")} OK')
