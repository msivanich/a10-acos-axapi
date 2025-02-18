#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_snmp_server_enable
description:
    - Enable SNMP service
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
    service:
        description:
        - "Enable SNMP service"
        type: bool
        required: False
    uuid:
        description:
        - "uuid of the object"
        type: str
        required: False
    traps:
        description:
        - "Field traps"
        type: dict
        required: False
        suboptions:
            all:
                description:
                - "Enable all SNMP traps"
                type: bool
            lldp:
                description:
                - "Enable lldp traps"
                type: bool
            uuid:
                description:
                - "uuid of the object"
                type: str
            routing:
                description:
                - "Field routing"
                type: dict
            gslb:
                description:
                - "Field gslb"
                type: dict
            slb:
                description:
                - "Field slb"
                type: dict
            snmp:
                description:
                - "Field snmp"
                type: dict
            vrrp_a:
                description:
                - "Field vrrp_a"
                type: dict
            vcs:
                description:
                - "Field vcs"
                type: dict
            system:
                description:
                - "Field system"
                type: dict
            slb_change:
                description:
                - "Field slb_change"
                type: dict
            lsn:
                description:
                - "Field lsn"
                type: dict
            network:
                description:
                - "Field network"
                type: dict
            ssl:
                description:
                - "Field ssl"
                type: dict

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
    "service",
    "traps",
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
        'service': {
            'type': 'bool',
        },
        'uuid': {
            'type': 'str',
        },
        'traps': {
            'type': 'dict',
            'all': {
                'type': 'bool',
            },
            'lldp': {
                'type': 'bool',
            },
            'uuid': {
                'type': 'str',
            },
            'routing': {
                'type': 'dict',
                'bgp': {
                    'type': 'dict',
                    'bgpEstablishedNotification': {
                        'type': 'bool',
                    },
                    'bgpBackwardTransNotification': {
                        'type': 'bool',
                    },
                    'uuid': {
                        'type': 'str',
                    }
                },
                'isis': {
                    'type': 'dict',
                    'isisAdjacencyChange': {
                        'type': 'bool',
                    },
                    'isisAreaMismatch': {
                        'type': 'bool',
                    },
                    'isisAttemptToExceedMaxSequence': {
                        'type': 'bool',
                    },
                    'isisAuthenticationFailure': {
                        'type': 'bool',
                    },
                    'isisAuthenticationTypeFailure': {
                        'type': 'bool',
                    },
                    'isisCorruptedLSPDetected': {
                        'type': 'bool',
                    },
                    'isisDatabaseOverload': {
                        'type': 'bool',
                    },
                    'isisIDLenMismatch': {
                        'type': 'bool',
                    },
                    'isisLSPTooLargeToPropagate': {
                        'type': 'bool',
                    },
                    'isisManualAddressDrops': {
                        'type': 'bool',
                    },
                    'isisMaxAreaAddressesMismatch': {
                        'type': 'bool',
                    },
                    'isisOriginatingLSPBufferSizeMismatch': {
                        'type': 'bool',
                    },
                    'isisOwnLSPPurge': {
                        'type': 'bool',
                    },
                    'isisProtocolsSupportedMismatch': {
                        'type': 'bool',
                    },
                    'isisRejectedAdjacency': {
                        'type': 'bool',
                    },
                    'isisSequenceNumberSkip': {
                        'type': 'bool',
                    },
                    'isisVersionSkew': {
                        'type': 'bool',
                    },
                    'uuid': {
                        'type': 'str',
                    }
                },
                'ospf': {
                    'type': 'dict',
                    'ospfIfAuthFailure': {
                        'type': 'bool',
                    },
                    'ospfIfConfigError': {
                        'type': 'bool',
                    },
                    'ospfIfRxBadPacket': {
                        'type': 'bool',
                    },
                    'ospfIfStateChange': {
                        'type': 'bool',
                    },
                    'ospfLsdbApproachingOverflow': {
                        'type': 'bool',
                    },
                    'ospfLsdbOverflow': {
                        'type': 'bool',
                    },
                    'ospfMaxAgeLsa': {
                        'type': 'bool',
                    },
                    'ospfNbrStateChange': {
                        'type': 'bool',
                    },
                    'ospfOriginateLsa': {
                        'type': 'bool',
                    },
                    'ospfTxRetransmit': {
                        'type': 'bool',
                    },
                    'ospfVirtIfAuthFailure': {
                        'type': 'bool',
                    },
                    'ospfVirtIfConfigError': {
                        'type': 'bool',
                    },
                    'ospfVirtIfRxBadPacket': {
                        'type': 'bool',
                    },
                    'ospfVirtIfStateChange': {
                        'type': 'bool',
                    },
                    'ospfVirtIfTxRetransmit': {
                        'type': 'bool',
                    },
                    'ospfVirtNbrStateChange': {
                        'type': 'bool',
                    },
                    'uuid': {
                        'type': 'str',
                    }
                }
            },
            'gslb': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'zone': {
                    'type': 'bool',
                },
                'site': {
                    'type': 'bool',
                },
                'group': {
                    'type': 'bool',
                },
                'service_ip': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'slb': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'application_buffer_limit': {
                    'type': 'bool',
                },
                'gateway_up': {
                    'type': 'bool',
                },
                'gateway_down': {
                    'type': 'bool',
                },
                'server_conn_limit': {
                    'type': 'bool',
                },
                'server_conn_resume': {
                    'type': 'bool',
                },
                'server_up': {
                    'type': 'bool',
                },
                'server_down': {
                    'type': 'bool',
                },
                'server_disabled': {
                    'type': 'bool',
                },
                'server_selection_failure': {
                    'type': 'bool',
                },
                'service_conn_limit': {
                    'type': 'bool',
                },
                'service_conn_resume': {
                    'type': 'bool',
                },
                'service_down': {
                    'type': 'bool',
                },
                'service_up': {
                    'type': 'bool',
                },
                'service_group_up': {
                    'type': 'bool',
                },
                'service_group_down': {
                    'type': 'bool',
                },
                'service_group_member_up': {
                    'type': 'bool',
                },
                'service_group_member_down': {
                    'type': 'bool',
                },
                'vip_connlimit': {
                    'type': 'bool',
                },
                'vip_connratelimit': {
                    'type': 'bool',
                },
                'vip_down': {
                    'type': 'bool',
                },
                'vip_port_connlimit': {
                    'type': 'bool',
                },
                'vip_port_connratelimit': {
                    'type': 'bool',
                },
                'vip_port_down': {
                    'type': 'bool',
                },
                'vip_port_up': {
                    'type': 'bool',
                },
                'vip_up': {
                    'type': 'bool',
                },
                'bw_rate_limit_exceed': {
                    'type': 'bool',
                },
                'bw_rate_limit_resume': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'snmp': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'linkdown': {
                    'type': 'bool',
                },
                'linkup': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'vrrp_a': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'active': {
                    'type': 'bool',
                },
                'standby': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'vcs': {
                'type': 'dict',
                'state_change': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'system': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'control_cpu_high': {
                    'type': 'bool',
                },
                'data_cpu_high': {
                    'type': 'bool',
                },
                'fan': {
                    'type': 'bool',
                },
                'file_sys_read_only': {
                    'type': 'bool',
                },
                'high_disk_use': {
                    'type': 'bool',
                },
                'high_memory_use': {
                    'type': 'bool',
                },
                'high_temp': {
                    'type': 'bool',
                },
                'low_temp': {
                    'type': 'bool',
                },
                'license_management': {
                    'type': 'bool',
                },
                'packet_drop': {
                    'type': 'bool',
                },
                'power': {
                    'type': 'bool',
                },
                'pri_disk': {
                    'type': 'bool',
                },
                'restart': {
                    'type': 'bool',
                },
                'sec_disk': {
                    'type': 'bool',
                },
                'shutdown': {
                    'type': 'bool',
                },
                'smp_resource_event': {
                    'type': 'bool',
                },
                'syslog_severity_one': {
                    'type': 'bool',
                },
                'tacacs_server_up_down': {
                    'type': 'bool',
                },
                'start': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'slb_change': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'resource_usage_warning': {
                    'type': 'bool',
                },
                'connection_resource_event': {
                    'type': 'bool',
                },
                'server': {
                    'type': 'bool',
                },
                'server_port': {
                    'type': 'bool',
                },
                'ssl_cert_change': {
                    'type': 'bool',
                },
                'ssl_cert_expire': {
                    'type': 'bool',
                },
                'vip': {
                    'type': 'bool',
                },
                'vip_port': {
                    'type': 'bool',
                },
                'system_threshold': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'lsn': {
                'type': 'dict',
                'all': {
                    'type': 'bool',
                },
                'total_port_usage_threshold': {
                    'type': 'bool',
                },
                'per_ip_port_usage_threshold': {
                    'type': 'bool',
                },
                'max_port_threshold': {
                    'type': 'int',
                },
                'max_ipport_threshold': {
                    'type': 'int',
                },
                'fixed_nat_port_mapping_file_change': {
                    'type': 'bool',
                },
                'traffic_exceeded': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'network': {
                'type': 'dict',
                'trunk_port_threshold': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'ssl': {
                'type': 'dict',
                'server_certificate_error': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/snmp-server/enable"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/snmp-server/enable"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["enable"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["enable"].get(k) != v:
            change_results["changed"] = True
            config_changes["enable"][k] = v

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
    payload = utils.build_json("enable", module.params, AVAILABLE_PROPERTIES)
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
                    "enable"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "enable-list"] if info != "NotFound" else info
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
