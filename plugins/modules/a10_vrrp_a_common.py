#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_vrrp_a_common
description:
    - HA VRRP-A Global Commands
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
    device_id:
        description:
        - "Unique ID for each VRRP-A box (Device-id number)"
        type: int
        required: False
    set_id:
        description:
        - "Set-ID for HA configuration (Set id from 1 to 15)"
        type: int
        required: False
    disable_default_vrid:
        description:
        - "Disable default vrid"
        type: bool
        required: False
    action:
        description:
        - "'enable'= enable vrrp-a; 'disable'= disable vrrp-a;"
        type: str
        required: False
    hello_interval:
        description:
        - "VRRP-A Hello Interval (1-255, in unit of 100millisec, default is 2)"
        type: int
        required: False
    preemption_delay:
        description:
        - "Delay before changing state from Active to Standby (1-255, in unit of
          100millisec, default is 60)"
        type: int
        required: False
    dead_timer:
        description:
        - "VRRP-A dead timer in terms of how many hello messages missed, default is 5
          (2-255, default is 5)"
        type: int
        required: False
    arp_retry:
        description:
        - "Number of additional gratuitous ARPs sent out after HA failover (1-255, default
          is 4)"
        type: int
        required: False
    track_event_delay:
        description:
        - "Delay before changing state after up/down event (Units of 100 milliseconds
          (default 30))"
        type: int
        required: False
    get_ready_time:
        description:
        - "set get ready time after ax starting up (60-1200, in unit of 100millisec,
          default is 60)"
        type: int
        required: False
    inline_mode_cfg:
        description:
        - "Field inline_mode_cfg"
        type: dict
        required: False
        suboptions:
            inline_mode:
                description:
                - "Enable Layer 2 Inline Hot Standby Mode"
                type: bool
            preferred_port:
                description:
                - "Preferred ethernet Port"
                type: str
            preferred_trunk:
                description:
                - "Preferred trunk Port"
                type: int
    restart_time:
        description:
        - "Time between restarting ports on standby system after transition"
        type: int
        required: False
    hostid_append_to_vrid:
        description:
        - "Field hostid_append_to_vrid"
        type: dict
        required: False
        suboptions:
            hostid_append_to_vrid_default:
                description:
                - "hostid append to vrid default"
                type: bool
            hostid_append_to_vrid_value:
                description:
                - "hostid append to vrid num"
                type: int
    forward_l4_packet_on_standby:
        description:
        - "Enables Layer 2/3 forwarding of Layer 4 traffic on the Standby ACOS device"
        type: bool
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
            vrrp_common_dummy:
                description:
                - "dummy counter"
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
    "action",
    "arp_retry",
    "dead_timer",
    "device_id",
    "disable_default_vrid",
    "forward_l4_packet_on_standby",
    "get_ready_time",
    "hello_interval",
    "hostid_append_to_vrid",
    "inline_mode_cfg",
    "preemption_delay",
    "restart_time",
    "set_id",
    "stats",
    "track_event_delay",
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
        'device_id': {
            'type': 'int',
        },
        'set_id': {
            'type': 'int',
        },
        'disable_default_vrid': {
            'type': 'bool',
        },
        'action': {
            'type': 'str',
            'choices': ['enable', 'disable']
        },
        'hello_interval': {
            'type': 'int',
        },
        'preemption_delay': {
            'type': 'int',
        },
        'dead_timer': {
            'type': 'int',
        },
        'arp_retry': {
            'type': 'int',
        },
        'track_event_delay': {
            'type': 'int',
        },
        'get_ready_time': {
            'type': 'int',
        },
        'inline_mode_cfg': {
            'type': 'dict',
            'inline_mode': {
                'type': 'bool',
            },
            'preferred_port': {
                'type': 'str',
            },
            'preferred_trunk': {
                'type': 'int',
            }
        },
        'restart_time': {
            'type': 'int',
        },
        'hostid_append_to_vrid': {
            'type': 'dict',
            'hostid_append_to_vrid_default': {
                'type': 'bool',
            },
            'hostid_append_to_vrid_value': {
                'type': 'int',
            }
        },
        'forward_l4_packet_on_standby': {
            'type': 'bool',
        },
        'uuid': {
            'type': 'str',
        },
        'stats': {
            'type': 'dict',
            'vrrp_common_dummy': {
                'type': 'str',
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/vrrp-a/common"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/vrrp-a/common"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["common"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["common"].get(k) != v:
            change_results["changed"] = True
            config_changes["common"][k] = v

    change_results["modified_values"].update(**config_changes)
    return change_results


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
    payload = utils.build_json("common", module.params, AVAILABLE_PROPERTIES)
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
                    "common"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "common-list"] if info != "NotFound" else info
            elif module.params.get("get_type") == "stats":
                get_type_result = api_client.get_stats(module.client,
                                                       existing_url(module),
                                                       params=module.params)
                result["axapi_calls"].append(get_type_result)
                info = get_type_result["response_body"]
                result["acos_info"] = info["common"][
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
