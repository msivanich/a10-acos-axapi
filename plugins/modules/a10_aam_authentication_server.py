#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_aam_authentication_server
description:
    - Authentication server configuration
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
    ldap:
        description:
        - "Field ldap"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            sampling_enable:
                description:
                - "Field sampling_enable"
                type: list
            instance_list:
                description:
                - "Field instance_list"
                type: list
    ocsp:
        description:
        - "Field ocsp"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            sampling_enable:
                description:
                - "Field sampling_enable"
                type: list
            instance_list:
                description:
                - "Field instance_list"
                type: list
    radius:
        description:
        - "Field radius"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            sampling_enable:
                description:
                - "Field sampling_enable"
                type: list
            instance_list:
                description:
                - "Field instance_list"
                type: list
    windows:
        description:
        - "Field windows"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            sampling_enable:
                description:
                - "Field sampling_enable"
                type: list
            instance_list:
                description:
                - "Field instance_list"
                type: list
    oper:
        description:
        - "Field oper"
        type: dict
        required: False
        suboptions:
            rserver_count:
                description:
                - "Field rserver_count"
                type: int
            rport_count:
                description:
                - "Field rport_count"
                type: int
            rserver_list:
                description:
                - "Field rserver_list"
                type: list
            name:
                description:
                - "Field name"
                type: str
            part_id:
                description:
                - "Field part_id"
                type: int
            get_count:
                description:
                - "Field get_count"
                type: str
            ldap:
                description:
                - "Field ldap"
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
    "ldap",
    "ocsp",
    "oper",
    "radius",
    "uuid",
    "windows",
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
        'ldap': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'sampling_enable': {
                'type': 'list',
                'counters1': {
                    'type':
                    'str',
                    'choices': [
                        'all', 'admin-bind-success', 'admin-bind-failure',
                        'bind-success', 'bind-failure', 'search-success',
                        'search-failure', 'authorize-success',
                        'authorize-failure', 'timeout-error', 'other-error',
                        'request', 'request-normal', 'request-dropped',
                        'response-success', 'response-failure',
                        'response-error', 'response-timeout', 'response-other',
                        'job-start-error', 'polling-control-error',
                        'ssl-session-created', 'ssl-session-failure',
                        'ldaps-idle-conn-num', 'ldaps-inuse-conn-num',
                        'pw-expiry', 'pw-change-success', 'pw-change-failure'
                    ]
                }
            },
            'instance_list': {
                'type': 'list',
                'name': {
                    'type': 'str',
                    'required': True,
                },
                'host': {
                    'type': 'dict',
                    'hostip': {
                        'type': 'str',
                    },
                    'hostipv6': {
                        'type': 'str',
                    }
                },
                'base': {
                    'type': 'str',
                },
                'port': {
                    'type': 'int',
                },
                'port_hm': {
                    'type': 'str',
                },
                'port_hm_disable': {
                    'type': 'bool',
                },
                'pwdmaxage': {
                    'type': 'int',
                },
                'admin_dn': {
                    'type': 'str',
                },
                'admin_secret': {
                    'type': 'bool',
                },
                'secret_string': {
                    'type': 'str',
                },
                'encrypted': {
                    'type': 'str',
                },
                'timeout': {
                    'type': 'int',
                },
                'dn_attribute': {
                    'type': 'str',
                },
                'default_domain': {
                    'type': 'str',
                },
                'bind_with_dn': {
                    'type': 'bool',
                },
                'derive_bind_dn': {
                    'type': 'dict',
                    'username_attr': {
                        'type': 'str',
                    }
                },
                'health_check': {
                    'type': 'bool',
                },
                'health_check_string': {
                    'type': 'str',
                },
                'health_check_disable': {
                    'type': 'bool',
                },
                'protocol': {
                    'type': 'str',
                    'choices': ['ldap', 'ldaps', 'starttls']
                },
                'ca_cert': {
                    'type': 'str',
                },
                'ldaps_conn_reuse_idle_timeout': {
                    'type': 'int',
                },
                'auth_type': {
                    'type': 'str',
                    'choices': ['ad', 'open-ldap']
                },
                'prompt_pw_change_before_exp': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                },
                'sampling_enable': {
                    'type': 'list',
                    'counters1': {
                        'type':
                        'str',
                        'choices': [
                            'all', 'admin-bind-success', 'admin-bind-failure',
                            'bind-success', 'bind-failure', 'search-success',
                            'search-failure', 'authorize-success',
                            'authorize-failure', 'timeout-error',
                            'other-error', 'request', 'ssl-session-created',
                            'ssl-session-failure', 'pw_expiry',
                            'pw_change_success', 'pw_change_failure'
                        ]
                    }
                }
            }
        },
        'ocsp': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'sampling_enable': {
                'type': 'list',
                'counters1': {
                    'type':
                    'str',
                    'choices': [
                        'all', 'stapling-certificate-good',
                        'stapling-certificate-revoked',
                        'stapling-certificate-unknown',
                        'stapling-request-normal', 'stapling-request-dropped',
                        'stapling-response-success',
                        'stapling-response-failure', 'stapling-response-error',
                        'stapling-response-timeout', 'stapling-response-other',
                        'request-normal', 'request-dropped',
                        'response-success', 'response-failure',
                        'response-error', 'response-timeout', 'response-other',
                        'job-start-error', 'polling-control-error'
                    ]
                }
            },
            'instance_list': {
                'type': 'list',
                'name': {
                    'type': 'str',
                    'required': True,
                },
                'url': {
                    'type': 'str',
                },
                'responder_ca': {
                    'type': 'str',
                },
                'responder_cert': {
                    'type': 'str',
                },
                'health_check': {
                    'type': 'bool',
                },
                'health_check_string': {
                    'type': 'str',
                },
                'health_check_disable': {
                    'type': 'bool',
                },
                'port_health_check': {
                    'type': 'str',
                },
                'port_health_check_disable': {
                    'type': 'bool',
                },
                'http_version': {
                    'type': 'bool',
                },
                'version_type': {
                    'type': 'str',
                    'choices': ['1.1']
                },
                'uuid': {
                    'type': 'str',
                },
                'sampling_enable': {
                    'type': 'list',
                    'counters1': {
                        'type':
                        'str',
                        'choices': [
                            'all', 'request', 'certificate-good',
                            'certificate-revoked', 'certificate-unknown',
                            'timeout', 'fail', 'stapling-request',
                            'stapling-certificate-good',
                            'stapling-certificate-revoked',
                            'stapling-certificate-unknown', 'stapling-timeout',
                            'stapling-fail'
                        ]
                    }
                }
            }
        },
        'radius': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'sampling_enable': {
                'type': 'list',
                'counters1': {
                    'type':
                    'str',
                    'choices': [
                        'all', 'authen_success', 'authen_failure',
                        'authorize_success', 'authorize_failure',
                        'access_challenge', 'timeout_error', 'other_error',
                        'request', 'request-normal', 'request-dropped',
                        'response-success', 'response-failure',
                        'response-error', 'response-timeout', 'response-other',
                        'job-start-error', 'polling-control-error',
                        'accounting-request-sent', 'accounting-success',
                        'accounting-failure'
                    ]
                }
            },
            'instance_list': {
                'type': 'list',
                'name': {
                    'type': 'str',
                    'required': True,
                },
                'host': {
                    'type': 'dict',
                    'hostip': {
                        'type': 'str',
                    },
                    'hostipv6': {
                        'type': 'str',
                    }
                },
                'secret': {
                    'type': 'bool',
                },
                'secret_string': {
                    'type': 'str',
                },
                'encrypted': {
                    'type': 'str',
                },
                'port': {
                    'type': 'int',
                },
                'port_hm': {
                    'type': 'str',
                },
                'port_hm_disable': {
                    'type': 'bool',
                },
                'interval': {
                    'type': 'int',
                },
                'retry': {
                    'type': 'int',
                },
                'health_check': {
                    'type': 'bool',
                },
                'health_check_string': {
                    'type': 'str',
                },
                'health_check_disable': {
                    'type': 'bool',
                },
                'accounting_port': {
                    'type': 'int',
                },
                'acct_port_hm': {
                    'type': 'str',
                },
                'acct_port_hm_disable': {
                    'type': 'bool',
                },
                'auth_type': {
                    'type': 'str',
                    'choices': ['pap', 'mschapv2', 'mschapv2-pap']
                },
                'uuid': {
                    'type': 'str',
                },
                'sampling_enable': {
                    'type': 'list',
                    'counters1': {
                        'type':
                        'str',
                        'choices': [
                            'all', 'authen_success', 'authen_failure',
                            'authorize_success', 'authorize_failure',
                            'access_challenge', 'timeout_error', 'other_error',
                            'request', 'accounting-request-sent',
                            'accounting-success', 'accounting-failure'
                        ]
                    }
                }
            }
        },
        'windows': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'sampling_enable': {
                'type': 'list',
                'counters1': {
                    'type':
                    'str',
                    'choices': [
                        'all', 'kerberos-request-send',
                        'kerberos-response-get', 'kerberos-timeout-error',
                        'kerberos-other-error', 'ntlm-authentication-success',
                        'ntlm-authentication-failure',
                        'ntlm-proto-negotiation-success',
                        'ntlm-proto-negotiation-failure',
                        'ntlm-session-setup-success',
                        'ntlm-session-setup-failed', 'kerberos-request-normal',
                        'kerberos-request-dropped',
                        'kerberos-response-success',
                        'kerberos-response-failure', 'kerberos-response-error',
                        'kerberos-response-timeout', 'kerberos-response-other',
                        'kerberos-job-start-error',
                        'kerberos-polling-control-error',
                        'ntlm-prepare-req-success', 'ntlm-prepare-req-failed',
                        'ntlm-timeout-error', 'ntlm-other-error',
                        'ntlm-request-normal', 'ntlm-request-dropped',
                        'ntlm-response-success', 'ntlm-response-failure',
                        'ntlm-response-error', 'ntlm-response-timeout',
                        'ntlm-response-other', 'ntlm-job-start-error',
                        'ntlm-polling-control-error', 'kerberos-pw-expiry',
                        'kerberos-pw-change-success',
                        'kerberos-pw-change-failure'
                    ]
                }
            },
            'instance_list': {
                'type': 'list',
                'name': {
                    'type': 'str',
                    'required': True,
                },
                'host': {
                    'type': 'dict',
                    'hostip': {
                        'type': 'str',
                    },
                    'hostipv6': {
                        'type': 'str',
                    }
                },
                'timeout': {
                    'type': 'int',
                },
                'auth_protocol': {
                    'type': 'dict',
                    'ntlm_disable': {
                        'type': 'bool',
                    },
                    'ntlm_version': {
                        'type': 'int',
                    },
                    'ntlm_health_check': {
                        'type': 'str',
                    },
                    'ntlm_health_check_disable': {
                        'type': 'bool',
                    },
                    'kerberos_disable': {
                        'type': 'bool',
                    },
                    'kerberos_port': {
                        'type': 'int',
                    },
                    'kport_hm': {
                        'type': 'str',
                    },
                    'kport_hm_disable': {
                        'type': 'bool',
                    },
                    'kerberos_password_change_port': {
                        'type': 'int',
                    }
                },
                'realm': {
                    'type': 'str',
                },
                'support_apacheds_kdc': {
                    'type': 'bool',
                },
                'health_check': {
                    'type': 'bool',
                },
                'health_check_string': {
                    'type': 'str',
                },
                'health_check_disable': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                },
                'sampling_enable': {
                    'type': 'list',
                    'counters1': {
                        'type':
                        'str',
                        'choices': [
                            'all', 'krb_send_req_success',
                            'krb_get_resp_success', 'krb_timeout_error',
                            'krb_other_error', 'krb_pw_expiry',
                            'krb_pw_change_success', 'krb_pw_change_failure',
                            'ntlm_proto_nego_success',
                            'ntlm_proto_nego_failure',
                            'ntlm_session_setup_success',
                            'ntlm_session_setup_failure',
                            'ntlm_prepare_req_success',
                            'ntlm_prepare_req_error', 'ntlm_auth_success',
                            'ntlm_auth_failure', 'ntlm_timeout_error',
                            'ntlm_other_error'
                        ]
                    }
                }
            }
        },
        'oper': {
            'type': 'dict',
            'rserver_count': {
                'type': 'int',
            },
            'rport_count': {
                'type': 'int',
            },
            'rserver_list': {
                'type': 'list',
                'server_name': {
                    'type': 'str',
                },
                'host': {
                    'type': 'str',
                },
                'ip': {
                    'type': 'str',
                },
                'hm': {
                    'type': 'str',
                },
                'status': {
                    'type': 'str',
                },
                'max_conn': {
                    'type': 'int',
                },
                'weight': {
                    'type': 'int',
                },
                'rport_list': {
                    'type': 'list',
                    'port': {
                        'type': 'int',
                    },
                    'protocol': {
                        'type': 'str',
                    },
                    'port_state': {
                        'type': 'str',
                    },
                    'port_hm': {
                        'type': 'str',
                    },
                    'port_status': {
                        'type': 'str',
                    },
                    'port_max_conn': {
                        'type': 'int',
                    },
                    'port_weight': {
                        'type': 'int',
                    },
                    'sg_list': {
                        'type': 'list',
                        'sg_name': {
                            'type': 'str',
                        },
                        'sg_state': {
                            'type': 'str',
                        }
                    }
                }
            },
            'name': {
                'type': 'str',
            },
            'part_id': {
                'type': 'int',
            },
            'get_count': {
                'type': 'str',
            },
            'ldap': {
                'type': 'dict',
                'oper': {
                    'type': 'dict',
                    'ldaps_server_list': {
                        'type': 'list',
                        'ldap_uri': {
                            'type': 'str',
                        },
                        'ldaps_idle_conn_num': {
                            'type': 'int',
                        },
                        'ldaps_idle_conn_fd_list': {
                            'type': 'str',
                        },
                        'ldaps_inuse_conn_num': {
                            'type': 'int',
                        },
                        'ldaps_inuse_conn_fd_list': {
                            'type': 'str',
                        }
                    }
                }
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/aam/authentication/server"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/aam/authentication/server"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["server"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["server"].get(k) != v:
            change_results["changed"] = True
            config_changes["server"][k] = v

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
    payload = utils.build_json("server", module.params, AVAILABLE_PROPERTIES)
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
                    "server"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "server-list"] if info != "NotFound" else info
            elif module.params.get("get_type") == "oper":
                get_oper_result = api_client.get_oper(module.client,
                                                      existing_url(module),
                                                      params=module.params)
                result["axapi_calls"].append(get_oper_result)
                info = get_oper_result["response_body"]
                result["acos_info"] = info["server"][
                    "oper"] if info != "NotFound" else info
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
