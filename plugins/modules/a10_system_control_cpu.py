#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_system_control_cpu
description:
    - System control cpu information
author: A10 Networks 2021
options:
    state:
        description:
        - State of the object to be created.
        choices:
          - noop
          - present
          - absent
        type: str
        required: True
    ansible_host:
        description:
        - Host for AXAPI authentication
        type: str
        required: True
    ansible_username:
        description:
        - Username for AXAPI authentication
        type: str
        required: True
    ansible_password:
        description:
        - Password for AXAPI authentication
        type: str
        required: True
    ansible_port:
        description:
        - Port for AXAPI authentication
        type: int
        required: True
    a10_device_context_id:
        description:
        - Device ID for aVCS configuration
        choices: [1-8]
        type: int
        required: False
    a10_partition:
        description:
        - Destination/target partition for object/command
        type: str
        required: False
    uuid:
        description:
        - "uuid of the object"
        type: str
        required: False
    stats:
        description:
        - "Field stats"
        type: dict
        required: False
        suboptions:
            ctrl_cpu_number:
                description:
                - "Number of ctrl cpus"
                type: str
            cpu_1:
                description:
                - "Control CPU-1"
                type: str
            cpu_2:
                description:
                - "Control CPU-2"
                type: str
            cpu_3:
                description:
                - "Control CPU-3"
                type: str
            cpu_4:
                description:
                - "Control CPU-4"
                type: str
            cpu_5:
                description:
                - "Control CPU-5"
                type: str
            cpu_6:
                description:
                - "Control CPU-6"
                type: str
            cpu_7:
                description:
                - "Control CPU-7"
                type: str
            cpu_8:
                description:
                - "Control CPU-8"
                type: str
            cpu_9:
                description:
                - "Control CPU-9"
                type: str
            cpu_10:
                description:
                - "Control CPU-10"
                type: str
            cpu_11:
                description:
                - "Control CPU-11"
                type: str
            cpu_12:
                description:
                - "Control CPU-12"
                type: str
            cpu_13:
                description:
                - "Control CPU-13"
                type: str
            cpu_14:
                description:
                - "Control CPU-14"
                type: str
            cpu_15:
                description:
                - "Control CPU-15"
                type: str
            cpu_16:
                description:
                - "Control CPU-16"
                type: str
            cpu_17:
                description:
                - "Control CPU-17"
                type: str
            cpu_18:
                description:
                - "Control CPU-18"
                type: str
            cpu_19:
                description:
                - "Control CPU-19"
                type: str
            cpu_20:
                description:
                - "Control CPU-20"
                type: str
            cpu_21:
                description:
                - "Control CPU-21"
                type: str
            cpu_22:
                description:
                - "Control CPU-22"
                type: str
            cpu_23:
                description:
                - "Control CPU-23"
                type: str
            cpu_24:
                description:
                - "Control CPU-24"
                type: str
            cpu_25:
                description:
                - "Control CPU-25"
                type: str
            cpu_26:
                description:
                - "Control CPU-26"
                type: str
            cpu_27:
                description:
                - "Control CPU-27"
                type: str
            cpu_28:
                description:
                - "Control CPU-28"
                type: str
            cpu_29:
                description:
                - "Control CPU-29"
                type: str
            cpu_30:
                description:
                - "Control CPU-30"
                type: str
            cpu_31:
                description:
                - "Control CPU-31"
                type: str
            cpu_32:
                description:
                - "Control CPU-32"
                type: str
            cpu_33:
                description:
                - "Control CPU-33"
                type: str
            cpu_34:
                description:
                - "Control CPU-34"
                type: str
            cpu_35:
                description:
                - "Control CPU-35"
                type: str
            cpu_36:
                description:
                - "Control CPU-36"
                type: str
            cpu_37:
                description:
                - "Control CPU-37"
                type: str
            cpu_38:
                description:
                - "Control CPU-38"
                type: str
            cpu_39:
                description:
                - "Control CPU-39"
                type: str
            cpu_40:
                description:
                - "Control CPU-40"
                type: str
            cpu_41:
                description:
                - "Control CPU-41"
                type: str
            cpu_42:
                description:
                - "Control CPU-42"
                type: str
            cpu_43:
                description:
                - "Control CPU-43"
                type: str
            cpu_44:
                description:
                - "Control CPU-44"
                type: str
            cpu_45:
                description:
                - "Control CPU-45"
                type: str
            cpu_46:
                description:
                - "Control CPU-46"
                type: str
            cpu_47:
                description:
                - "Control CPU-47"
                type: str
            cpu_48:
                description:
                - "Control CPU-48"
                type: str
            cpu_49:
                description:
                - "Control CPU-49"
                type: str
            cpu_50:
                description:
                - "Control CPU-50"
                type: str
            cpu_51:
                description:
                - "Control CPU-51"
                type: str
            cpu_52:
                description:
                - "Control CPU-52"
                type: str
            cpu_53:
                description:
                - "Control CPU-53"
                type: str
            cpu_54:
                description:
                - "Control CPU-54"
                type: str
            cpu_55:
                description:
                - "Control CPU-55"
                type: str
            cpu_56:
                description:
                - "Control CPU-56"
                type: str
            cpu_57:
                description:
                - "Control CPU-57"
                type: str
            cpu_58:
                description:
                - "Control CPU-58"
                type: str
            cpu_59:
                description:
                - "Control CPU-59"
                type: str
            cpu_60:
                description:
                - "Control CPU-60"
                type: str
            cpu_61:
                description:
                - "Control CPU-61"
                type: str
            cpu_62:
                description:
                - "Control CPU-62"
                type: str
            cpu_63:
                description:
                - "Control CPU-63"
                type: str
            cpu_64:
                description:
                - "Control CPU-64"
                type: str

'''

RETURN = r'''
modified_values:
    description:
    - Values modified (or potential changes if using check_mode) as a result of task operation
    returned: changed
    type: dict
axapi_calls:
    description: Sequential list of AXAPI calls made by the task
    returned: always
    type: list
    elements: dict
    contains:
        endpoint:
            description: The AXAPI endpoint being accessed.
            type: str
            sample:
                - /axapi/v3/slb/virtual_server
                - /axapi/v3/file/ssl-cert
        http_method:
            description:
            - HTTP method being used by the primary task to interact with the AXAPI endpoint.
            type: str
            sample:
                - POST
                - GET
        request_body:
            description: Params used to query the AXAPI
            type: complex
        response_body:
            description: Response from the AXAPI
            type: complex
'''

EXAMPLES = """
"""

import copy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.a10.acos_axapi.plugins.module_utils import \
    errors as a10_ex
from ansible_collections.a10.acos_axapi.plugins.module_utils import \
    wrapper as api_client
from ansible_collections.a10.acos_axapi.plugins.module_utils import \
    utils
from ansible_collections.a10.acos_axapi.plugins.module_utils.client import \
    client_factory
from ansible_collections.a10.acos_axapi.plugins.module_utils.kwbl import \
    KW_OUT, translate_blacklist as translateBlacklist

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = [
    "stats",
    "uuid",
]


def get_default_argspec():
    return dict(
        ansible_host=dict(type='str', required=True),
        ansible_username=dict(type='str', required=True),
        ansible_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str',
                   default="present",
                   choices=['noop', 'present', 'absent']),
        ansible_port=dict(type='int', choices=[80, 443], required=True),
        a10_partition=dict(
            type='str',
            required=False,
        ),
        a10_device_context_id=dict(
            type='int',
            choices=[1, 2, 3, 4, 5, 6, 7, 8],
            required=False,
        ),
        get_type=dict(type='str', choices=["single", "list", "oper", "stats"]),
    )


def get_argspec():
    rv = get_default_argspec()
    rv.update({
        'uuid': {
            'type': 'str',
        },
        'stats': {
            'type': 'dict',
            'ctrl_cpu_number': {
                'type': 'str',
            },
            'cpu_1': {
                'type': 'str',
            },
            'cpu_2': {
                'type': 'str',
            },
            'cpu_3': {
                'type': 'str',
            },
            'cpu_4': {
                'type': 'str',
            },
            'cpu_5': {
                'type': 'str',
            },
            'cpu_6': {
                'type': 'str',
            },
            'cpu_7': {
                'type': 'str',
            },
            'cpu_8': {
                'type': 'str',
            },
            'cpu_9': {
                'type': 'str',
            },
            'cpu_10': {
                'type': 'str',
            },
            'cpu_11': {
                'type': 'str',
            },
            'cpu_12': {
                'type': 'str',
            },
            'cpu_13': {
                'type': 'str',
            },
            'cpu_14': {
                'type': 'str',
            },
            'cpu_15': {
                'type': 'str',
            },
            'cpu_16': {
                'type': 'str',
            },
            'cpu_17': {
                'type': 'str',
            },
            'cpu_18': {
                'type': 'str',
            },
            'cpu_19': {
                'type': 'str',
            },
            'cpu_20': {
                'type': 'str',
            },
            'cpu_21': {
                'type': 'str',
            },
            'cpu_22': {
                'type': 'str',
            },
            'cpu_23': {
                'type': 'str',
            },
            'cpu_24': {
                'type': 'str',
            },
            'cpu_25': {
                'type': 'str',
            },
            'cpu_26': {
                'type': 'str',
            },
            'cpu_27': {
                'type': 'str',
            },
            'cpu_28': {
                'type': 'str',
            },
            'cpu_29': {
                'type': 'str',
            },
            'cpu_30': {
                'type': 'str',
            },
            'cpu_31': {
                'type': 'str',
            },
            'cpu_32': {
                'type': 'str',
            },
            'cpu_33': {
                'type': 'str',
            },
            'cpu_34': {
                'type': 'str',
            },
            'cpu_35': {
                'type': 'str',
            },
            'cpu_36': {
                'type': 'str',
            },
            'cpu_37': {
                'type': 'str',
            },
            'cpu_38': {
                'type': 'str',
            },
            'cpu_39': {
                'type': 'str',
            },
            'cpu_40': {
                'type': 'str',
            },
            'cpu_41': {
                'type': 'str',
            },
            'cpu_42': {
                'type': 'str',
            },
            'cpu_43': {
                'type': 'str',
            },
            'cpu_44': {
                'type': 'str',
            },
            'cpu_45': {
                'type': 'str',
            },
            'cpu_46': {
                'type': 'str',
            },
            'cpu_47': {
                'type': 'str',
            },
            'cpu_48': {
                'type': 'str',
            },
            'cpu_49': {
                'type': 'str',
            },
            'cpu_50': {
                'type': 'str',
            },
            'cpu_51': {
                'type': 'str',
            },
            'cpu_52': {
                'type': 'str',
            },
            'cpu_53': {
                'type': 'str',
            },
            'cpu_54': {
                'type': 'str',
            },
            'cpu_55': {
                'type': 'str',
            },
            'cpu_56': {
                'type': 'str',
            },
            'cpu_57': {
                'type': 'str',
            },
            'cpu_58': {
                'type': 'str',
            },
            'cpu_59': {
                'type': 'str',
            },
            'cpu_60': {
                'type': 'str',
            },
            'cpu_61': {
                'type': 'str',
            },
            'cpu_62': {
                'type': 'str',
            },
            'cpu_63': {
                'type': 'str',
            },
            'cpu_64': {
                'type': 'str',
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/system/control-cpu"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/system/control-cpu"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config):
    if existing_config:
        result["changed"] = True
    return result


def create(module, result, payload={}):
    call_result = api_client.post(module.client, new_url(module), payload)
    result["axapi_calls"].append(call_result)
    result["modified_values"].update(**call_result["response_body"])
    result["changed"] = True
    return result


def update(module, result, existing_config, payload={}):
    call_result = api_client.post(module.client, existing_url(module), payload)
    result["axapi_calls"].append(call_result)
    if call_result["response_body"] == existing_config:
        result["changed"] = False
    else:
        result["modified_values"].update(**call_result["response_body"])
        result["changed"] = True
    return result


def present(module, result, existing_config):
    payload = utils.build_json("control-cpu", module.params,
                               AVAILABLE_PROPERTIES)
    change_results = report_changes(module, result, existing_config, payload)
    if module.check_mode:
        return change_results
    elif not existing_config:
        return create(module, result, payload)
    elif existing_config and change_results.get('changed'):
        return update(module, result, existing_config, payload)
    return result


def delete(module, result):
    try:
        call_result = api_client.delete(module.client, existing_url(module))
        result["axapi_calls"].append(call_result)
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    return result


def absent(module, result, existing_config):
    if not existing_config:
        result["changed"] = False
        return result

    if module.check_mode:
        result["changed"] = True
        return result

    return delete(module, result)


def run_command(module):
    result = dict(changed=False,
                  messages="",
                  modified_values={},
                  axapi_calls=[],
                  ansible_facts={},
                  acos_info={})

    state = module.params["state"]
    ansible_host = module.params["ansible_host"]
    ansible_username = module.params["ansible_username"]
    ansible_password = module.params["ansible_password"]
    ansible_port = module.params["ansible_port"]
    a10_partition = module.params["a10_partition"]
    a10_device_context_id = module.params["a10_device_context_id"]

    if ansible_port == 80:
        protocol = "http"
    elif ansible_port == 443:
        protocol = "https"

    module.client = client_factory(ansible_host, ansible_port, protocol,
                                   ansible_username, ansible_password)

    valid = True

    run_errors = []
    if state == 'present':
        requires_one_of = sorted([])
        valid, validation_errors = utils.validate(module.params,
                                                  requires_one_of)
        for ve in validation_errors:
            run_errors.append(ve)

    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    try:
        if a10_partition:
            result["axapi_calls"].append(
                api_client.active_partition(module.client, a10_partition))

        if a10_device_context_id:
            result["axapi_calls"].append(
                api_client.switch_device_context(module.client,
                                                 a10_device_context_id))

        existing_config = api_client.get(module.client, existing_url(module))
        result["axapi_calls"].append(existing_config)
        if existing_config['response_body'] != 'NotFound':
            existing_config = existing_config["response_body"]
        else:
            existing_config = None

        if state == 'present':
            result = present(module, result, existing_config)

        if state == 'absent':
            result = absent(module, result, existing_config)

        if state == 'noop':
            if module.params.get("get_type") == "single":
                get_result = api_client.get(module.client,
                                            existing_url(module))
                result["axapi_calls"].append(get_result)
                info = get_result["response_body"]
                result["acos_info"] = info[
                    "control-cpu"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "control-cpu-list"] if info != "NotFound" else info
            elif module.params.get("get_type") == "stats":
                get_type_result = api_client.get_stats(module.client,
                                                       existing_url(module),
                                                       params=module.params)
                result["axapi_calls"].append(get_type_result)
                info = get_type_result["response_body"]
                result["acos_info"] = info["control-cpu"][
                    "stats"] if info != "NotFound" else info
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    finally:
        if module.client.auth_session.session_id:
            module.client.auth_session.close()

    return result


def main():
    module = AnsibleModule(argument_spec=get_argspec(),
                           supports_check_mode=True)
    result = run_command(module)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
