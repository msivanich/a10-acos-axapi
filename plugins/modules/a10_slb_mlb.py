#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_slb_mlb
description:
    - Configure mlb
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
                - "'all'= all; 'client_msg_sent'= Client message sent; 'server_msg_received'=
          Server message received; 'server_conn_created'= Server connection created;
          'server_conn_rst'= Server connection reset; 'server_conn_failed'= Server
          connection failed; 'server_conn_closed'= Server connection closed;
          'client_conn_created'= Client connection created; 'client_conn_closed'= Client
          connection closed; 'client_conn_not_found'= Client connection not found;
          'msg_dropped'= Message dropped; 'mlb_dcmsg_sent'= Dcmsg sent;
          'mlb_dcmsg_received'= Dcmsg received; 'mlb_dcmsg_error'= Dcmsg error;
          'mlb_dcmsg_alloc'= Dcmsg alloc; 'mlb_dcmsg_free'= Dcmsg free;"
                type: str
    oper:
        description:
        - "Field oper"
        type: dict
        required: False
        suboptions:
            l4_cpu_list:
                description:
                - "Field l4_cpu_list"
                type: list
            cpu_count:
                description:
                - "Field cpu_count"
                type: int
    stats:
        description:
        - "Field stats"
        type: dict
        required: False
        suboptions:
            client_msg_sent:
                description:
                - "Client message sent"
                type: str
            server_msg_received:
                description:
                - "Server message received"
                type: str
            server_conn_created:
                description:
                - "Server connection created"
                type: str
            server_conn_rst:
                description:
                - "Server connection reset"
                type: str
            server_conn_failed:
                description:
                - "Server connection failed"
                type: str
            server_conn_closed:
                description:
                - "Server connection closed"
                type: str
            client_conn_created:
                description:
                - "Client connection created"
                type: str
            client_conn_closed:
                description:
                - "Client connection closed"
                type: str
            client_conn_not_found:
                description:
                - "Client connection not found"
                type: str
            msg_dropped:
                description:
                - "Message dropped"
                type: str
            mlb_dcmsg_sent:
                description:
                - "Dcmsg sent"
                type: str
            mlb_dcmsg_received:
                description:
                - "Dcmsg received"
                type: str
            mlb_dcmsg_error:
                description:
                - "Dcmsg error"
                type: str
            mlb_dcmsg_alloc:
                description:
                - "Dcmsg alloc"
                type: str
            mlb_dcmsg_free:
                description:
                - "Dcmsg free"
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
    "oper",
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
                    'all', 'client_msg_sent', 'server_msg_received',
                    'server_conn_created', 'server_conn_rst',
                    'server_conn_failed', 'server_conn_closed',
                    'client_conn_created', 'client_conn_closed',
                    'client_conn_not_found', 'msg_dropped', 'mlb_dcmsg_sent',
                    'mlb_dcmsg_received', 'mlb_dcmsg_error', 'mlb_dcmsg_alloc',
                    'mlb_dcmsg_free'
                ]
            }
        },
        'oper': {
            'type': 'dict',
            'l4_cpu_list': {
                'type': 'list',
                'client_msg_sent': {
                    'type': 'int',
                },
                'server_msg_received': {
                    'type': 'int',
                },
                'server_conn_created': {
                    'type': 'int',
                },
                'server_conn_rst': {
                    'type': 'int',
                },
                'server_conn_failed': {
                    'type': 'int',
                },
                'server_conn_closed': {
                    'type': 'int',
                },
                'client_conn_created': {
                    'type': 'int',
                },
                'client_conn_closed': {
                    'type': 'int',
                },
                'client_conn_not_found': {
                    'type': 'int',
                },
                'msg_dropped': {
                    'type': 'int',
                },
                'mlb_dcmsg_sent': {
                    'type': 'int',
                },
                'mlb_dcmsg_received': {
                    'type': 'int',
                },
                'mlb_dcmsg_error': {
                    'type': 'int',
                },
                'mlb_dcmsg_alloc': {
                    'type': 'int',
                },
                'mlb_dcmsg_free': {
                    'type': 'int',
                }
            },
            'cpu_count': {
                'type': 'int',
            }
        },
        'stats': {
            'type': 'dict',
            'client_msg_sent': {
                'type': 'str',
            },
            'server_msg_received': {
                'type': 'str',
            },
            'server_conn_created': {
                'type': 'str',
            },
            'server_conn_rst': {
                'type': 'str',
            },
            'server_conn_failed': {
                'type': 'str',
            },
            'server_conn_closed': {
                'type': 'str',
            },
            'client_conn_created': {
                'type': 'str',
            },
            'client_conn_closed': {
                'type': 'str',
            },
            'client_conn_not_found': {
                'type': 'str',
            },
            'msg_dropped': {
                'type': 'str',
            },
            'mlb_dcmsg_sent': {
                'type': 'str',
            },
            'mlb_dcmsg_received': {
                'type': 'str',
            },
            'mlb_dcmsg_error': {
                'type': 'str',
            },
            'mlb_dcmsg_alloc': {
                'type': 'str',
            },
            'mlb_dcmsg_free': {
                'type': 'str',
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/slb/mlb"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/slb/mlb"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["mlb"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["mlb"].get(k) != v:
            change_results["changed"] = True
            config_changes["mlb"][k] = v

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
    payload = utils.build_json("mlb", module.params, AVAILABLE_PROPERTIES)
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
                result[
                    "acos_info"] = info["mlb"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "mlb-list"] if info != "NotFound" else info
            elif module.params.get("get_type") == "oper":
                get_oper_result = api_client.get_oper(module.client,
                                                      existing_url(module),
                                                      params=module.params)
                result["axapi_calls"].append(get_oper_result)
                info = get_oper_result["response_body"]
                result["acos_info"] = info["mlb"][
                    "oper"] if info != "NotFound" else info
            elif module.params.get("get_type") == "stats":
                get_type_result = api_client.get_stats(module.client,
                                                       existing_url(module),
                                                       params=module.params)
                result["axapi_calls"].append(get_type_result)
                info = get_type_result["response_body"]
                result["acos_info"] = info["mlb"][
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
