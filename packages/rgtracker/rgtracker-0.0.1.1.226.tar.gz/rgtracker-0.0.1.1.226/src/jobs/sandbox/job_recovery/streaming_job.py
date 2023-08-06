from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.pageviews import *
from rgtracker.uniquedevices import *
from redisgears import executeCommand as execute

def compare_versions_sandbox(v1, v2):
    # None version is less then all version
    if v1 is None:
        return -1
    if v2 is None:
        return 1

    if v1 == "99.99.99":
        return 1
    if v2 == "99.99.99":
        return -1

    v1_major, v1_minor, v1_patch = v1.split(".")
    v2_major, v2_minor, v2_patch = v2.split(".")

    if int(v1_major) > int(v2_major):
        return 1
    elif int(v1_major) < int(v2_major):
        return -1

    if int(v1_minor) > int(v2_minor):
        return 1
    elif int(v1_minor) < int(v2_minor):
        return -1

    if int(v1_patch) > int(v2_patch):
        return 1
    elif int(v1_patch) < int(v2_patch):
        return -1

    return 0

def unregister_old_versions_sandbox(name, version):
    tracker_log(f"Unregister old version of {name}")
    registrations = execute("RG.DUMPREGISTRATIONS")
    for registration in registrations:
        registration_dict = registration_arr_to_dict(registration, 0)
        desc_str = registration_dict["desc"]
        try:
            desc = json.loads(desc_str)
        except Exception as e:
            continue
        if "name" in desc.keys() and name in desc["name"]:
            tracker_log(
                "Version auto upgrade is not atomic, make sure to use it when is not traffic to the database (otherwise you might lose events).",
                log_level="warning"
            )
            if "version" not in desc.keys():
                execute("RG.UNREGISTER", registration_dict["id"])
                tracker_log(f"Unregister {registration_dict['id']}")
                continue
            v = desc["version"]
            if compare_versions_sandbox(version, v) > 0:
                execute("RG.UNREGISTER", registration_dict["id"])
                tracker_log(f"Unregistered {registration_dict['id']}")
            else:
                raise Exception(
                    "Found a version which is greater or equals current version, aborting."
                )
    tracker_log("Unregistered old versions.")

# unregister_old_versions_sandbox("StreamReaderJob", '99.99.99')

descJson = {
    "name": f"StreamReaderJob",
    "version": '0.0.2',
    "desc": f"Lorem Ipsum",
}

unregister_old_versions_sandbox(descJson.get('name'), descJson.get('version'))

GB("StreamReader", desc=json.dumps(descJson)). \
    foreach(lambda record: tracker_log(f'{record}', f'{descJson.get("name")} - {descJson.get("version")} - ')). \
    register(
    prefix=f'ST:TRACKER::::',
    convertToStr=True,
    collect=True,
    onFailedPolicy='abort',
    onFailedRetryInterval=1,
    batch=1,
    duration=0,
    trimStream=False)
