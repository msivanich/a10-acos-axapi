#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_interface_ethernet_ipv6_ospf
description:
    - Open Shortest Path First for IPv6 (OSPFv3)
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
    ethernet_ifnum:
        description:
        - Key to identify parent object
        type: str
        required: True
    network_list:
        description:
        - "Field network_list"
        type: list
        required: False
        suboptions:
            broadcast_type:
                description:
                - "'broadcast'= Specify OSPF broadcast multi-access network; 'non-broadcast'=
          Specify OSPF NBMA network; 'point-to-point'= Specify OSPF point-to-point
          network; 'point-to-multipoint'= Specify OSPF point-to-multipoint network;"
                type: str
            p2mp_nbma:
                description:
                - "Specify non-broadcast point-to-multipoint network"
                type: bool
            network_instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    bfd:
        description:
        - "Bidirectional Forwarding Detection (BFD)"
        type: bool
        required: False
    disable:
        description:
        - "Disable BFD"
        type: bool
        required: False
    cost_cfg:
        description:
        - "Field cost_cfg"
        type: list
        required: False
        suboptions:
            cost:
                description:
                - "Interface cost"
                type: int
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    dead_interval_cfg:
        description:
        - "Field dead_interval_cfg"
        type: list
        required: False
        suboptions:
            dead_interval:
                description:
                - "Interval after which a neighbor is declared dead (Seconds)"
                type: int
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    hello_interval_cfg:
        description:
        - "Field hello_interval_cfg"
        type: list
        required: False
        suboptions:
            hello_interval:
                description:
                - "Time between HELLO packets (Seconds)"
                type: int
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    mtu_ignore_cfg:
        description:
        - "Field mtu_ignore_cfg"
        type: list
        required: False
        suboptions:
            mtu_ignore:
                description:
                - "Ignores the MTU in DBD packets"
                type: bool
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    neighbor_cfg:
        description:
        - "Field neighbor_cfg"
        type: list
        required: False
        suboptions:
            neighbor:
                description:
                - "OSPFv3 neighbor (Neighbor IPv6 address)"
                type: str
            neig_inst:
                description:
                - "Specify the interface instance ID"
                type: int
            neighbor_cost:
                description:
                - "OSPF cost for point-to-multipoint neighbor (metric)"
                type: int
            neighbor_poll_interval:
                description:
                - "OSPF dead-router polling interval (Seconds)"
                type: int
            neighbor_priority:
                description:
                - "OSPF priority of non-broadcast neighbor"
                type: int
    priority_cfg:
        description:
        - "Field priority_cfg"
        type: list
        required: False
        suboptions:
            priority:
                description:
                - "Router priority"
                type: int
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    retransmit_interval_cfg:
        description:
        - "Field retransmit_interval_cfg"
        type: list
        required: False
        suboptions:
            retransmit_interval:
                description:
                - "Time between retransmitting lost link state advertisements (Seconds)"
                type: int
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    transmit_delay_cfg:
        description:
        - "Field transmit_delay_cfg"
        type: list
        required: False
        suboptions:
            transmit_delay:
                description:
                - "Link state transmit delay (Seconds)"
                type: int
            instance_id:
                description:
                - "Specify the interface instance ID"
                type: int
    uuid:
        description:
        - "uuid of the object"
        type: str
        required: False

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
    "bfd",
    "cost_cfg",
    "dead_interval_cfg",
    "disable",
    "hello_interval_cfg",
    "mtu_ignore_cfg",
    "neighbor_cfg",
    "network_list",
    "priority_cfg",
    "retransmit_interval_cfg",
    "transmit_delay_cfg",
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
        'network_list': {
            'type': 'list',
            'broadcast_type': {
                'type':
                'str',
                'choices': [
                    'broadcast', 'non-broadcast', 'point-to-point',
                    'point-to-multipoint'
                ]
            },
            'p2mp_nbma': {
                'type': 'bool',
            },
            'network_instance_id': {
                'type': 'int',
            }
        },
        'bfd': {
            'type': 'bool',
        },
        'disable': {
            'type': 'bool',
        },
        'cost_cfg': {
            'type': 'list',
            'cost': {
                'type': 'int',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'dead_interval_cfg': {
            'type': 'list',
            'dead_interval': {
                'type': 'int',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'hello_interval_cfg': {
            'type': 'list',
            'hello_interval': {
                'type': 'int',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'mtu_ignore_cfg': {
            'type': 'list',
            'mtu_ignore': {
                'type': 'bool',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'neighbor_cfg': {
            'type': 'list',
            'neighbor': {
                'type': 'str',
            },
            'neig_inst': {
                'type': 'int',
            },
            'neighbor_cost': {
                'type': 'int',
            },
            'neighbor_poll_interval': {
                'type': 'int',
            },
            'neighbor_priority': {
                'type': 'int',
            }
        },
        'priority_cfg': {
            'type': 'list',
            'priority': {
                'type': 'int',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'retransmit_interval_cfg': {
            'type': 'list',
            'retransmit_interval': {
                'type': 'int',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'transmit_delay_cfg': {
            'type': 'list',
            'transmit_delay': {
                'type': 'int',
            },
            'instance_id': {
                'type': 'int',
            }
        },
        'uuid': {
            'type': 'str',
        }
    })
    # Parent keys
    rv.update(dict(ethernet_ifnum=dict(type='str', required=True), ))
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/interface/ethernet/{ethernet_ifnum}/ipv6/ospf"

    f_dict = {}
    f_dict["ethernet_ifnum"] = module.params["ethernet_ifnum"]

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/interface/ethernet/{ethernet_ifnum}/ipv6/ospf"

    f_dict = {}
    f_dict["ethernet_ifnum"] = module.params["ethernet_ifnum"]

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["ospf"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["ospf"].get(k) != v:
            change_results["changed"] = True
            config_changes["ospf"][k] = v

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
    payload = utils.build_json("ospf", module.params, AVAILABLE_PROPERTIES)
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
                    "acos_info"] = info["ospf"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "ospf-list"] if info != "NotFound" else info
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
