#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_interface_trunk_ip
description:
    - Global IP configuration subcommands
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
    trunk_ifnum:
        description:
        - Key to identify parent object
        type: str
        required: True
    dhcp:
        description:
        - "Use DHCP to configure IP address"
        type: bool
        required: False
    address_list:
        description:
        - "Field address_list"
        type: list
        required: False
        suboptions:
            ipv4_address:
                description:
                - "IP address"
                type: str
            ipv4_netmask:
                description:
                - "IP subnet mask"
                type: str
    allow_promiscuous_vip:
        description:
        - "Allow traffic to be associated with promiscuous VIP"
        type: bool
        required: False
    client:
        description:
        - "Client facing interface for IPv4/v6 traffic"
        type: bool
        required: False
    server:
        description:
        - "Server facing interface for IPv4/v6 traffic"
        type: bool
        required: False
    cache_spoofing_port:
        description:
        - "This interface connects to spoofing cache"
        type: bool
        required: False
    helper_address_list:
        description:
        - "Field helper_address_list"
        type: list
        required: False
        suboptions:
            helper_address:
                description:
                - "Helper address for DHCP packets (IP address)"
                type: str
    nat:
        description:
        - "Field nat"
        type: dict
        required: False
        suboptions:
            inside:
                description:
                - "Configure interface as inside"
                type: bool
            outside:
                description:
                - "Configure interface as outside"
                type: bool
    ttl_ignore:
        description:
        - "Ignore TTL decrement for a received packet"
        type: bool
        required: False
    slb_partition_redirect:
        description:
        - "Redirect SLB traffic across partition"
        type: bool
        required: False
    generate_membership_query:
        description:
        - "Enable Membership Query"
        type: bool
        required: False
    query_interval:
        description:
        - "1 - 255 (Default is 125)"
        type: int
        required: False
    max_resp_time:
        description:
        - "Maximum Response Time (Max Response Time (Default is 100))"
        type: int
        required: False
    uuid:
        description:
        - "uuid of the object"
        type: str
        required: False
    stateful_firewall:
        description:
        - "Field stateful_firewall"
        type: dict
        required: False
        suboptions:
            inside:
                description:
                - "Inside (private) interface for stateful firewall"
                type: bool
            class_list:
                description:
                - "Class List (Class List Name)"
                type: str
            outside:
                description:
                - "Outside (public) interface for stateful firewall"
                type: bool
            access_list:
                description:
                - "Access-list for traffic from the outside"
                type: bool
            acl_id:
                description:
                - "ACL id"
                type: int
            uuid:
                description:
                - "uuid of the object"
                type: str
    router:
        description:
        - "Field router"
        type: dict
        required: False
        suboptions:
            isis:
                description:
                - "Field isis"
                type: dict
    rip:
        description:
        - "Field rip"
        type: dict
        required: False
        suboptions:
            authentication:
                description:
                - "Field authentication"
                type: dict
            send_packet:
                description:
                - "Enable sending packets through the specified interface"
                type: bool
            receive_packet:
                description:
                - "Enable receiving packet through the specified interface"
                type: bool
            send_cfg:
                description:
                - "Field send_cfg"
                type: dict
            receive_cfg:
                description:
                - "Field receive_cfg"
                type: dict
            split_horizon_cfg:
                description:
                - "Field split_horizon_cfg"
                type: dict
            uuid:
                description:
                - "uuid of the object"
                type: str
    ospf:
        description:
        - "Field ospf"
        type: dict
        required: False
        suboptions:
            ospf_global:
                description:
                - "Field ospf_global"
                type: dict
            ospf_ip_list:
                description:
                - "Field ospf_ip_list"
                type: list

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
    "address_list",
    "allow_promiscuous_vip",
    "cache_spoofing_port",
    "client",
    "dhcp",
    "generate_membership_query",
    "helper_address_list",
    "max_resp_time",
    "nat",
    "ospf",
    "query_interval",
    "rip",
    "router",
    "server",
    "slb_partition_redirect",
    "stateful_firewall",
    "ttl_ignore",
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
        'dhcp': {
            'type': 'bool',
        },
        'address_list': {
            'type': 'list',
            'ipv4_address': {
                'type': 'str',
            },
            'ipv4_netmask': {
                'type': 'str',
            }
        },
        'allow_promiscuous_vip': {
            'type': 'bool',
        },
        'client': {
            'type': 'bool',
        },
        'server': {
            'type': 'bool',
        },
        'cache_spoofing_port': {
            'type': 'bool',
        },
        'helper_address_list': {
            'type': 'list',
            'helper_address': {
                'type': 'str',
            }
        },
        'nat': {
            'type': 'dict',
            'inside': {
                'type': 'bool',
            },
            'outside': {
                'type': 'bool',
            }
        },
        'ttl_ignore': {
            'type': 'bool',
        },
        'slb_partition_redirect': {
            'type': 'bool',
        },
        'generate_membership_query': {
            'type': 'bool',
        },
        'query_interval': {
            'type': 'int',
        },
        'max_resp_time': {
            'type': 'int',
        },
        'uuid': {
            'type': 'str',
        },
        'stateful_firewall': {
            'type': 'dict',
            'inside': {
                'type': 'bool',
            },
            'class_list': {
                'type': 'str',
            },
            'outside': {
                'type': 'bool',
            },
            'access_list': {
                'type': 'bool',
            },
            'acl_id': {
                'type': 'int',
            },
            'uuid': {
                'type': 'str',
            }
        },
        'router': {
            'type': 'dict',
            'isis': {
                'type': 'dict',
                'tag': {
                    'type': 'str',
                },
                'uuid': {
                    'type': 'str',
                }
            }
        },
        'rip': {
            'type': 'dict',
            'authentication': {
                'type': 'dict',
                'str': {
                    'type': 'dict',
                    'string': {
                        'type': 'str',
                    }
                },
                'mode': {
                    'type': 'dict',
                    'mode': {
                        'type': 'str',
                        'choices': ['md5', 'text']
                    }
                },
                'key_chain': {
                    'type': 'dict',
                    'key_chain': {
                        'type': 'str',
                    }
                }
            },
            'send_packet': {
                'type': 'bool',
            },
            'receive_packet': {
                'type': 'bool',
            },
            'send_cfg': {
                'type': 'dict',
                'send': {
                    'type': 'bool',
                },
                'version': {
                    'type': 'str',
                    'choices': ['1', '2', '1-compatible', '1-2']
                }
            },
            'receive_cfg': {
                'type': 'dict',
                'receive': {
                    'type': 'bool',
                },
                'version': {
                    'type': 'str',
                    'choices': ['1', '2', '1-2']
                }
            },
            'split_horizon_cfg': {
                'type': 'dict',
                'state': {
                    'type': 'str',
                    'choices': ['poisoned', 'disable', 'enable']
                }
            },
            'uuid': {
                'type': 'str',
            }
        },
        'ospf': {
            'type': 'dict',
            'ospf_global': {
                'type': 'dict',
                'authentication_cfg': {
                    'type': 'dict',
                    'authentication': {
                        'type': 'bool',
                    },
                    'value': {
                        'type': 'str',
                        'choices': ['message-digest', 'null']
                    }
                },
                'authentication_key': {
                    'type': 'str',
                },
                'bfd_cfg': {
                    'type': 'dict',
                    'bfd': {
                        'type': 'bool',
                    },
                    'disable': {
                        'type': 'bool',
                    }
                },
                'cost': {
                    'type': 'int',
                },
                'database_filter_cfg': {
                    'type': 'dict',
                    'database_filter': {
                        'type': 'str',
                        'choices': ['all']
                    },
                    'out': {
                        'type': 'bool',
                    }
                },
                'dead_interval': {
                    'type': 'int',
                },
                'disable': {
                    'type': 'str',
                    'choices': ['all']
                },
                'hello_interval': {
                    'type': 'int',
                },
                'message_digest_cfg': {
                    'type': 'list',
                    'message_digest_key': {
                        'type': 'int',
                    },
                    'md5': {
                        'type': 'dict',
                        'md5_value': {
                            'type': 'str',
                        },
                        'encrypted': {
                            'type': 'str',
                        }
                    }
                },
                'mtu': {
                    'type': 'int',
                },
                'mtu_ignore': {
                    'type': 'bool',
                },
                'network': {
                    'type': 'dict',
                    'broadcast': {
                        'type': 'bool',
                    },
                    'non_broadcast': {
                        'type': 'bool',
                    },
                    'point_to_point': {
                        'type': 'bool',
                    },
                    'point_to_multipoint': {
                        'type': 'bool',
                    },
                    'p2mp_nbma': {
                        'type': 'bool',
                    }
                },
                'priority': {
                    'type': 'int',
                },
                'retransmit_interval': {
                    'type': 'int',
                },
                'transmit_delay': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'ospf_ip_list': {
                'type': 'list',
                'ip_addr': {
                    'type': 'str',
                    'required': True,
                },
                'authentication': {
                    'type': 'bool',
                },
                'value': {
                    'type': 'str',
                    'choices': ['message-digest', 'null']
                },
                'authentication_key': {
                    'type': 'str',
                },
                'cost': {
                    'type': 'int',
                },
                'database_filter': {
                    'type': 'str',
                    'choices': ['all']
                },
                'out': {
                    'type': 'bool',
                },
                'dead_interval': {
                    'type': 'int',
                },
                'hello_interval': {
                    'type': 'int',
                },
                'message_digest_cfg': {
                    'type': 'list',
                    'message_digest_key': {
                        'type': 'int',
                    },
                    'md5_value': {
                        'type': 'str',
                    },
                    'encrypted': {
                        'type': 'str',
                    }
                },
                'mtu_ignore': {
                    'type': 'bool',
                },
                'priority': {
                    'type': 'int',
                },
                'retransmit_interval': {
                    'type': 'int',
                },
                'transmit_delay': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                }
            }
        }
    })
    # Parent keys
    rv.update(dict(trunk_ifnum=dict(type='str', required=True), ))
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/interface/trunk/{trunk_ifnum}/ip"

    f_dict = {}
    f_dict["trunk_ifnum"] = module.params["trunk_ifnum"]

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/interface/trunk/{trunk_ifnum}/ip"

    f_dict = {}
    f_dict["trunk_ifnum"] = module.params["trunk_ifnum"]

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["ip"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["ip"].get(k) != v:
            change_results["changed"] = True
            config_changes["ip"][k] = v

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
    payload = utils.build_json("ip", module.params, AVAILABLE_PROPERTIES)
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
                    "acos_info"] = info["ip"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "ip-list"] if info != "NotFound" else info
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
