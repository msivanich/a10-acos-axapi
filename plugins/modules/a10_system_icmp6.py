#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_system_icmp6
description:
    - Display ICMPv6 statistics
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
    sampling_enable:
        description:
        - "Field sampling_enable"
        type: list
        required: False
        suboptions:
            counters1:
                description:
                - "'all'= all; 'in_msgs'= In messages; 'in_errors'= In Errors; 'in_dest_un_reach'=
          In Destunation Unreachable; 'in_pkt_too_big'= In Packet too big;
          'in_time_exceeds'= In TTL Exceeds; 'in_param_prob'= In Parameter Problem;
          'in_echoes'= In Echo requests; 'in_exho_reply'= In Echo replies;
          'in_grp_mem_query'= In Group member query; 'in_grp_mem_resp'= In Group member
          reply; 'in_grp_mem_reduction'= In Group member reduction; 'in_router_sol'= In
          Router solicitation; 'in_ra'= In Router advertisement; 'in_ns'= In neighbor
          solicitation; 'in_na'= In neighbor advertisement; 'in_redirect'= In Redirects;
          'out_msg'= Out Messages; 'out_dst_un_reach'= Out Destination Unreachable;
          'out_pkt_too_big'= Out Packet too big; 'out_time_exceeds'= Out TTL Exceeds;
          'out_param_prob'= Out Parameter Problem; 'out_echo_req'= Out Echo requests;
          'out_echo_replies'= Out Echo replies; 'out_rs'= Out Router solicitation;
          'out_ra'= Out Router advertisement; 'out_ns'= Out neighbor solicitation;
          'out_na'= Out neighbor advertisement; 'out_redirects'= Out Redirects;
          'out_mem_resp'= Out Group member reply; 'out_mem_reductions'= Out Group member
          reduction; 'err_rs'= Error Router solicitation; 'err_ra'= Error Router
          advertisement; 'err_ns'= Error Neighbor solicitation; 'err_na'= Error Neighbor
          advertisement; 'err_redirects'= Error Redirects; 'err_echoes'= Error Echo
          requests; 'err_echo_replies'= Error Echo replies;"
                type: str
    stats:
        description:
        - "Field stats"
        type: dict
        required: False
        suboptions:
            in_msgs:
                description:
                - "In messages"
                type: str
            in_errors:
                description:
                - "In Errors"
                type: str
            in_dest_un_reach:
                description:
                - "In Destunation Unreachable"
                type: str
            in_pkt_too_big:
                description:
                - "In Packet too big"
                type: str
            in_time_exceeds:
                description:
                - "In TTL Exceeds"
                type: str
            in_param_prob:
                description:
                - "In Parameter Problem"
                type: str
            in_echoes:
                description:
                - "In Echo requests"
                type: str
            in_exho_reply:
                description:
                - "In Echo replies"
                type: str
            in_grp_mem_query:
                description:
                - "In Group member query"
                type: str
            in_grp_mem_resp:
                description:
                - "In Group member reply"
                type: str
            in_grp_mem_reduction:
                description:
                - "In Group member reduction"
                type: str
            in_router_sol:
                description:
                - "In Router solicitation"
                type: str
            in_ra:
                description:
                - "In Router advertisement"
                type: str
            in_ns:
                description:
                - "In neighbor solicitation"
                type: str
            in_na:
                description:
                - "In neighbor advertisement"
                type: str
            in_redirect:
                description:
                - "In Redirects"
                type: str
            out_msg:
                description:
                - "Out Messages"
                type: str
            out_dst_un_reach:
                description:
                - "Out Destination Unreachable"
                type: str
            out_pkt_too_big:
                description:
                - "Out Packet too big"
                type: str
            out_time_exceeds:
                description:
                - "Out TTL Exceeds"
                type: str
            out_param_prob:
                description:
                - "Out Parameter Problem"
                type: str
            out_echo_req:
                description:
                - "Out Echo requests"
                type: str
            out_echo_replies:
                description:
                - "Out Echo replies"
                type: str
            out_rs:
                description:
                - "Out Router solicitation"
                type: str
            out_ra:
                description:
                - "Out Router advertisement"
                type: str
            out_ns:
                description:
                - "Out neighbor solicitation"
                type: str
            out_na:
                description:
                - "Out neighbor advertisement"
                type: str
            out_redirects:
                description:
                - "Out Redirects"
                type: str
            out_mem_resp:
                description:
                - "Out Group member reply"
                type: str
            out_mem_reductions:
                description:
                - "Out Group member reduction"
                type: str
            err_rs:
                description:
                - "Error Router solicitation"
                type: str
            err_ra:
                description:
                - "Error Router advertisement"
                type: str
            err_ns:
                description:
                - "Error Neighbor solicitation"
                type: str
            err_na:
                description:
                - "Error Neighbor advertisement"
                type: str
            err_redirects:
                description:
                - "Error Redirects"
                type: str
            err_echoes:
                description:
                - "Error Echo requests"
                type: str
            err_echo_replies:
                description:
                - "Error Echo replies"
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
    "sampling_enable",
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
        'sampling_enable': {
            'type': 'list',
            'counters1': {
                'type':
                'str',
                'choices': [
                    'all', 'in_msgs', 'in_errors', 'in_dest_un_reach',
                    'in_pkt_too_big', 'in_time_exceeds', 'in_param_prob',
                    'in_echoes', 'in_exho_reply', 'in_grp_mem_query',
                    'in_grp_mem_resp', 'in_grp_mem_reduction', 'in_router_sol',
                    'in_ra', 'in_ns', 'in_na', 'in_redirect', 'out_msg',
                    'out_dst_un_reach', 'out_pkt_too_big', 'out_time_exceeds',
                    'out_param_prob', 'out_echo_req', 'out_echo_replies',
                    'out_rs', 'out_ra', 'out_ns', 'out_na', 'out_redirects',
                    'out_mem_resp', 'out_mem_reductions', 'err_rs', 'err_ra',
                    'err_ns', 'err_na', 'err_redirects', 'err_echoes',
                    'err_echo_replies'
                ]
            }
        },
        'stats': {
            'type': 'dict',
            'in_msgs': {
                'type': 'str',
            },
            'in_errors': {
                'type': 'str',
            },
            'in_dest_un_reach': {
                'type': 'str',
            },
            'in_pkt_too_big': {
                'type': 'str',
            },
            'in_time_exceeds': {
                'type': 'str',
            },
            'in_param_prob': {
                'type': 'str',
            },
            'in_echoes': {
                'type': 'str',
            },
            'in_exho_reply': {
                'type': 'str',
            },
            'in_grp_mem_query': {
                'type': 'str',
            },
            'in_grp_mem_resp': {
                'type': 'str',
            },
            'in_grp_mem_reduction': {
                'type': 'str',
            },
            'in_router_sol': {
                'type': 'str',
            },
            'in_ra': {
                'type': 'str',
            },
            'in_ns': {
                'type': 'str',
            },
            'in_na': {
                'type': 'str',
            },
            'in_redirect': {
                'type': 'str',
            },
            'out_msg': {
                'type': 'str',
            },
            'out_dst_un_reach': {
                'type': 'str',
            },
            'out_pkt_too_big': {
                'type': 'str',
            },
            'out_time_exceeds': {
                'type': 'str',
            },
            'out_param_prob': {
                'type': 'str',
            },
            'out_echo_req': {
                'type': 'str',
            },
            'out_echo_replies': {
                'type': 'str',
            },
            'out_rs': {
                'type': 'str',
            },
            'out_ra': {
                'type': 'str',
            },
            'out_ns': {
                'type': 'str',
            },
            'out_na': {
                'type': 'str',
            },
            'out_redirects': {
                'type': 'str',
            },
            'out_mem_resp': {
                'type': 'str',
            },
            'out_mem_reductions': {
                'type': 'str',
            },
            'err_rs': {
                'type': 'str',
            },
            'err_ra': {
                'type': 'str',
            },
            'err_ns': {
                'type': 'str',
            },
            'err_na': {
                'type': 'str',
            },
            'err_redirects': {
                'type': 'str',
            },
            'err_echoes': {
                'type': 'str',
            },
            'err_echo_replies': {
                'type': 'str',
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/system/icmp6"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/system/icmp6"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["icmp6"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["icmp6"].get(k) != v:
            change_results["changed"] = True
            config_changes["icmp6"][k] = v

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
    payload = utils.build_json("icmp6", module.params, AVAILABLE_PROPERTIES)
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
                    "icmp6"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "icmp6-list"] if info != "NotFound" else info
            elif module.params.get("get_type") == "stats":
                get_type_result = api_client.get_stats(module.client,
                                                       existing_url(module),
                                                       params=module.params)
                result["axapi_calls"].append(get_type_result)
                info = get_type_result["response_body"]
                result["acos_info"] = info["icmp6"][
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
