from rgtracker.common import *
import math
import pandas as pd
from redisgears import executeCommand as execute
from redisgears import log


def extract(record, dimension):
    return record['value']['dimension'] == dimension


def transform(records, number_of_rotated_keys, dimension):
    df = pd.DataFrame(records)
    df['ids'] = df['ids'].apply(lambda x: json.loads(x) if x.startswith('[') else x)
    # tracker_log(f'all_ids - {df["ids"].values.tolist()}', f'W-UD-1to5 - transform - ')

    def flatten_list(A):
        rt = []
        for i in A:
            if isinstance(i, list):
                rt.extend(flatten_list(i))
            else:
                rt.append(i)
        return rt

    def unique_item(_list):
        return list(set(_list))

    grouped_df = df.groupby('ts').agg(lambda ids: unique_item(flatten_list(list(ids)))).sort_values('ts').reset_index()
    # tracker_log(f'all_ts - {grouped_df["ts"].values.tolist()}', f'W-PG-1to5 - transform - ')

    expected_rows = number_of_rotated_keys
    chunks = math.floor(len(grouped_df['ts']) / expected_rows + 1)
    i = 0
    j = expected_rows

    results = {
        'ids': [],
        'merge': [],
        'reinject': []
    }
    for x in range(chunks):
        df_sliced = grouped_df[i:j]
        if df_sliced.shape[0] >= number_of_rotated_keys:

            # Add only ids from 'complete' chunk
            ts = df_sliced["ts"].values.tolist()
            # tracker_log(f'chunk_{x}_ts - {ts}', f'X-PG-1to5 - transform - ')

            ids = df_sliced.apply(lambda ids: unique_item(flatten_list(ids)))['ids']
            for unique_id in ids:
                results.get('ids').append(unique_id)
            # tracker_log(f'chunk_{x}_ids - {ids}', f'X-PG-1to5 - transform - ')

            results.get('merge').append({
                'name': create_key_name(
                    Type.HLL.value,
                    '',
                    dimension,
                    '',
                    get_ts_df(ts[0], df_sliced["ts"]),
                    Metric.UNIQUE_DEVICES.value
                ),
                'keys': [create_key_name(Type.HLL.value, '', dimension, '', ts, Metric.UNIQUE_DEVICES.value) for ts in
                         df_sliced['ts']]
            })
        else:
            [results.get('reinject').append({
                'ts': row[1],
                'ids': row[0]
            }) for row in zip(df_sliced['ids'], df_sliced['ts'])]

        i += expected_rows
        j += expected_rows

    # Deduplicate ids
    results.update({'ids': list(set(results.get('ids')))})
    # tracker_log(f'final_ids - {results.get("ids")}', f'X-PG-1to5 - transform - ')
    return results


def load_device(job_name, records, dimension, write_to_ts, timeseries_name, key_expire_duration_sc, reinject_stream_name,
         output_stream_name):
    def get_ts(ts):
        if len(ts.split('_')) > 1:
            return ts.split("_")[-1]
        else:
            return ts

    # tracker_log(
    #     f'ids:{len(records.get("ids"))} merged:{len(records.get("merge"))} reinjected:{len(records.get("reinject"))}\n{records}',
    #     f'{job_name} - load - ')

    capped_stream = get_maxlen_capped_stream(timeseries_name, dimension)

    index_name = create_key_name(
        type=Type.INDEX.value,
        name='',
        dimension=dimension,
        record_id='',
        ts='',
        metric='')

    for hll_reinject in records.get('reinject'):
        execute('XADD', reinject_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                'ts', hll_reinject.get('ts'),
                'status', 'reinject',
                'ids', json.dumps(hll_reinject.get('ids')))
        # tracker_log(
        #     f'XADD {reinject_stream_name} * ts {hll_reinject.get("ts")} status reinject ids {json.dumps(hll_reinject.get("ids"))}',
        #     f'{job_name} - load - ')

    for hll_merge in records.get("merge"):
        # FixMe: useless EXISTS, merged key never exists. Example of merged key: HLL::W::1663581720000_1663582260000:UD
        # Move this into 'ids' loop?
        if execute('EXISTS', hll_merge.get('name')) != 1:

            parsed_key = parse_key_name(hll_merge.get('name'))
            for id in records.get('ids'):
                k = create_key_name(Type.HLL.value, '', dimension, id, parsed_key.get('ts'),
                                    Metric.UNIQUE_DEVICES.value)
                keys = [create_key_name(Type.HLL.value, '', dimension, id, parse_key_name(k).get('ts'),
                                        Metric.UNIQUE_DEVICES.value) for k in hll_merge.get('keys')]
                execute('PFMERGE', k, *keys)
                # tracker_log(f'PFMERGE {k} {keys}', f'{job_name} - load - ')

                if write_to_ts:
                    unique_devices = execute('PFCOUNT', *keys)
                    # tracker_log(f'PFCOUNT {keys}', f'{job_name} - load - ')

                    timeseries_key_name = create_key_name(
                        type=Type.TIMESERIES.value,
                        name=timeseries_name,
                        dimension=dimension,
                        record_id=id,
                        metric=Metric.UNIQUE_DEVICES.value)

                    if dimension == Dimension.WEBSITE.value:
                        # record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}',
                        #                        'RETURN', '3', 'name', 'AS', 'website_name')
                        # tracker_log(f'Get {dimension} infos - {record_infos}', f'{job_name} ')
                        json_key = create_key_name(Type.JSON.value, '', Dimension.WEBSITE.value, id, '', '')
                        # JSON.GET J::S:46535707faf945b66a11ddf37f8017b2c29bfa3e:: website.id website.name name
                        record_infos = execute('JSON.GET', json_key, 'name')
                        record_infos = json.loads(record_infos)

                        # FixMe: HOT FIX -> no records info found
                        if bool(record_infos):
                            execute('TS.ADD', timeseries_key_name, get_ts(parsed_key.get('ts')), unique_devices,
                                    'ON_DUPLICATE', 'LAST',
                                    'LABELS', 'ts_name', timeseries_name,
                                    'dimension', dimension, Dimension.METRIC.value, Metric.UNIQUE_DEVICES.value,
                                    'website_id', id, 'website_name', record_infos)
                            tracker_log(
                                f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                                f'{job_name} - ')
                        else:
                            tracker_log(
                                f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                                f'{job_name} - warning - ')
                    elif dimension == Dimension.SECTION.value:
                        # record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                        #                        'name', 'AS', 'section_name', 'website_id', 'website_name')
                        json_key = create_key_name(Type.JSON.value, '', Dimension.SECTION.value, id, '', '')
                        # JSON.GET J::S:46535707faf945b66a11ddf37f8017b2c29bfa3e:: website.id website.name name
                        record_infos = execute('JSON.GET', json_key, 'website.id', 'website.name', 'name')
                        record_infos = json.loads(record_infos)

                        # tracker_log(f'Get {dimension} infos - {record_infos}', f'{job_name} ')
                        # FixMe: HOT FIX -> no records info found
                        if bool(record_infos):
                            execute('TS.ADD', timeseries_key_name, get_ts(parsed_key.get("ts")), unique_devices,
                                    'ON_DUPLICATE', 'LAST',
                                    'LABELS', 'ts_name', timeseries_name,
                                    'dimension', dimension, Dimension.METRIC.value, Metric.UNIQUE_DEVICES.value,
                                    'section_id', id, 'section_name', record_infos.get('name'),
                                    'website_id', record_infos.get('website.id'), 'website_name', record_infos.get('website.name'))
                            tracker_log(
                                f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                                f'{job_name} - ')
                        else:
                            tracker_log(
                                f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                                f'{job_name} - warning - ')
                    elif dimension == Dimension.PAGE.value:
                        # record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                        #                        'website_id', 'website_name', 'section_id', 'section_name', 'article_id')
                        json_key = create_key_name(Type.JSON.value, '', Dimension.PAGE.value, id, '', '')
                        # JSON.GET J::P:620070307ea50a61c177f8c3dbb063b708dad92c:: website.id website.name section.id section.name article_id
                        record_infos = execute('JSON.GET', json_key, 'website.id', 'website.name', 'section.id', 'section.name', 'article_id')
                        record_infos = json.loads(record_infos)

                        # tracker_log(f'Get {dimension} infos - {record_infos}', f'{job_name} ')
                        if bool(record_infos):
                            execute('TS.ADD', timeseries_key_name, get_ts(parsed_key.get("ts")), unique_devices,
                                    'ON_DUPLICATE', 'LAST',
                                    'LABELS', 'ts_name', timeseries_name,
                                    'dimension', dimension, Dimension.METRIC.value, Metric.UNIQUE_DEVICES.value,
                                    'page_id', id,
                                    'website_id', record_infos.get('website.id'), 'website_name', record_infos.get('website.name'),
                                    'section_id', record_infos.get('section.id'), 'section_name', record_infos.get('section.name'),
                                    'article_id', record_infos.get('article_id'))
                            tracker_log(
                                f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                                f'{job_name} - ')
                        else:
                            tracker_log(
                                f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                                f'{job_name} - warning - ')

                execute('EXPIRE', k, key_expire_duration_sc)

            execute('XADD', output_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                    'ts', parsed_key.get('ts'),
                    'status', 'merged',
                    'ids', json.dumps(records.get('ids')))
            # tracker_log(f'Write key {hll_merge.get("name")} with ids {json.dumps(records.get("ids"))} to {output_stream_name} ', f'{job_name} - ')



    return records
