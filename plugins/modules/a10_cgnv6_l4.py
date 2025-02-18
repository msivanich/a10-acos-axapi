#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_cgnv6_l4
description:
    - CGNV6 L4 Statistics
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
                - "'all'= all; 'no-fwd-route'= No Forward Route for Session; 'no-rev-route'= No
          Reverse Route for Session; 'out-of-session-memory'= Out of Session Memory;
          'tcp-rst-sent'= TCP RST Sent; 'ipip-icmp-reply-sent'= IPIP ICMP Echo Reply
          Sent; 'icmp-filtered-sent'= ICMP Administratively Filtered Sent; 'icmp-host-
          unreachable-sent'= ICMP Host Unreachable Sent; 'icmp-reply-no-session-drop'=
          ICMP Reply No Session Drop; 'ipip-truncated'= IPIP Truncated Packet; 'ip-src-
          invalid-unicast'= IPv4 Source Not Valid Unicast; 'ip-dst-invalid-unicast'= IPv4
          Destination Not Valid Unicast; 'ipv6-src-invalid-unicast'= IPv6 Source Not
          Valid Unicast; 'ipv6-dst-invalid-unicast'= IPv6 Destination Not Valid Unicast;
          'bad-l3-protocol'= Bad Layer 3 Protocol; 'special-ipv4-no-route'= Stateless
          IPv4 No Forward Route; 'special-ipv6-no-route'= Stateless IPv6 No Forward
          Route; 'icmp-reply-sent'= ICMP Echo Reply Sent; 'icmpv6-reply-sent'= ICMPv6
          Echo Reply Sent; 'out-of-state-dropped'= L4 Out of State packets; 'ttl-
          exceeded-sent'= ICMP TTL Exceeded Sent; 'cross-cpu-alg-gre-no-match'= ALG GRE
          Cross CPU No Matching Session; 'cross-cpu-alg-gre-preprocess-err'= ALG GRE
          Cross CPU Preprocess Error; 'lsn-fast-setup'= LSN Fast Setup Attempt; 'lsn-
          fast-setup-err'= LSN Fast Setup Error; 'nat64-fast-setup'= NAT64 Fast Setup
          Attempt; 'nat64-fast-setup-err'= NAT64 Fast Setup Error; 'dslite-fast-setup'=
          DS-Lite Fast Setup Attempt; 'dslite-fast-setup-err'= DS-Lite Fast Setup Error;
          'fast-setup-delayed-err'= Fast Setup Delayed Error; 'fast-setup-mtu-too-small'=
          Fast Setup MTU Too Small; 'fixed-nat44-fast-setup'= Fixed NAT Fast Setup
          Attempt; 'fixed-nat44-fast-setup-err'= Fixed NAT Fast Setup Error; 'fixed-
          nat64-fast-setup'= Fixed NAT Fast Setup Attempt; 'fixed-nat64-fast-setup-err'=
          Fixed NAT Fast Setup Error; 'fixed-nat-dslite-fast-setup'= Fixed NAT Fast Setup
          Attempt; 'fixed-nat-dslite-fast-setup-err'= Fixed NAT Fast Setup Error; 'fixed-
          nat-fast-setup-delayed-err'= Fixed NAT Fast Setup Delayed Error; 'fixed-nat-
          fast-setup-mtu-too-small'= Fixed NAT Fast Setup MTU Too Small; 'static-nat-
          fast-setup'= Static NAT Fast Setup Attempt; 'static-nat-fast-setup-err'= Static
          NAT Fast Setup Error; 'dst-nat-needed-drop'= Destination NAT Needed Drop;
          'invalid-nat64-translated-addr'= Invalid NAT64 Translated IPv4 Address; 'tcp-
          rst-loop-drop'= RST Loop Drop; 'static-nat-alloc'= Static NAT Alloc; 'static-
          nat-free'= Static NAT Free; 'process-l4'= Process L4; 'preprocess-error'=
          Preprocess Error; 'process-special'= Process Special; 'process-continue'=
          Process Continue; 'process-error'= Process Error; 'fw-match-no-rule-drop'=
          Firewall Matched No CGNv6 Rule Drop; 'ip-unknown-process'= Process IP Unknown;
          'src-nat-pool-not-found'= Src NAT Pool Not Found; 'dst-nat-pool-not-found'= Dst
          NAT Pool Not Found; 'l3-ip-src-invalid-unicast'= IPv4 L3 Source Invalid
          Unicast; 'l3-ip-dst-invalid-unicast'= IPv4 L3 Destination Invalid Unicast;
          'l3-ipv6-src-invalid-unicast'= IPv6 L3 Source Invalid Unicast; 'l3-ipv6-dst-
          invalid-unicast'= IPv6 L3 Destination Invalid Unicast; 'fw-zone-mismatch-
          rerouting-drop'= Rerouting Zone Mismatch Drop; 'nat-range-list-acl-deny'= Nat
          range-list ACL deny; 'nat-range-list-acl-permit'= Nat range-list ACL permit;
          'fw-next-action-incorrect-drop'= FW Next Action Incorrect Drop;"
                type: str
    stats:
        description:
        - "Field stats"
        type: dict
        required: False
        suboptions:
            no_fwd_route:
                description:
                - "No Forward Route for Session"
                type: str
            no_rev_route:
                description:
                - "No Reverse Route for Session"
                type: str
            out_of_session_memory:
                description:
                - "Out of Session Memory"
                type: str
            tcp_rst_sent:
                description:
                - "TCP RST Sent"
                type: str
            ipip_icmp_reply_sent:
                description:
                - "IPIP ICMP Echo Reply Sent"
                type: str
            icmp_filtered_sent:
                description:
                - "ICMP Administratively Filtered Sent"
                type: str
            icmp_host_unreachable_sent:
                description:
                - "ICMP Host Unreachable Sent"
                type: str
            icmp_reply_no_session_drop:
                description:
                - "ICMP Reply No Session Drop"
                type: str
            ipip_truncated:
                description:
                - "IPIP Truncated Packet"
                type: str
            ip_src_invalid_unicast:
                description:
                - "IPv4 Source Not Valid Unicast"
                type: str
            ip_dst_invalid_unicast:
                description:
                - "IPv4 Destination Not Valid Unicast"
                type: str
            ipv6_src_invalid_unicast:
                description:
                - "IPv6 Source Not Valid Unicast"
                type: str
            ipv6_dst_invalid_unicast:
                description:
                - "IPv6 Destination Not Valid Unicast"
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
                    'all', 'no-fwd-route', 'no-rev-route',
                    'out-of-session-memory', 'tcp-rst-sent',
                    'ipip-icmp-reply-sent', 'icmp-filtered-sent',
                    'icmp-host-unreachable-sent', 'icmp-reply-no-session-drop',
                    'ipip-truncated', 'ip-src-invalid-unicast',
                    'ip-dst-invalid-unicast', 'ipv6-src-invalid-unicast',
                    'ipv6-dst-invalid-unicast', 'bad-l3-protocol',
                    'special-ipv4-no-route', 'special-ipv6-no-route',
                    'icmp-reply-sent', 'icmpv6-reply-sent',
                    'out-of-state-dropped', 'ttl-exceeded-sent',
                    'cross-cpu-alg-gre-no-match',
                    'cross-cpu-alg-gre-preprocess-err', 'lsn-fast-setup',
                    'lsn-fast-setup-err', 'nat64-fast-setup',
                    'nat64-fast-setup-err', 'dslite-fast-setup',
                    'dslite-fast-setup-err', 'fast-setup-delayed-err',
                    'fast-setup-mtu-too-small', 'fixed-nat44-fast-setup',
                    'fixed-nat44-fast-setup-err', 'fixed-nat64-fast-setup',
                    'fixed-nat64-fast-setup-err',
                    'fixed-nat-dslite-fast-setup',
                    'fixed-nat-dslite-fast-setup-err',
                    'fixed-nat-fast-setup-delayed-err',
                    'fixed-nat-fast-setup-mtu-too-small',
                    'static-nat-fast-setup', 'static-nat-fast-setup-err',
                    'dst-nat-needed-drop', 'invalid-nat64-translated-addr',
                    'tcp-rst-loop-drop', 'static-nat-alloc', 'static-nat-free',
                    'process-l4', 'preprocess-error', 'process-special',
                    'process-continue', 'process-error',
                    'fw-match-no-rule-drop', 'ip-unknown-process',
                    'src-nat-pool-not-found', 'dst-nat-pool-not-found',
                    'l3-ip-src-invalid-unicast', 'l3-ip-dst-invalid-unicast',
                    'l3-ipv6-src-invalid-unicast',
                    'l3-ipv6-dst-invalid-unicast',
                    'fw-zone-mismatch-rerouting-drop',
                    'nat-range-list-acl-deny', 'nat-range-list-acl-permit',
                    'fw-next-action-incorrect-drop'
                ]
            }
        },
        'stats': {
            'type': 'dict',
            'no_fwd_route': {
                'type': 'str',
            },
            'no_rev_route': {
                'type': 'str',
            },
            'out_of_session_memory': {
                'type': 'str',
            },
            'tcp_rst_sent': {
                'type': 'str',
            },
            'ipip_icmp_reply_sent': {
                'type': 'str',
            },
            'icmp_filtered_sent': {
                'type': 'str',
            },
            'icmp_host_unreachable_sent': {
                'type': 'str',
            },
            'icmp_reply_no_session_drop': {
                'type': 'str',
            },
            'ipip_truncated': {
                'type': 'str',
            },
            'ip_src_invalid_unicast': {
                'type': 'str',
            },
            'ip_dst_invalid_unicast': {
                'type': 'str',
            },
            'ipv6_src_invalid_unicast': {
                'type': 'str',
            },
            'ipv6_dst_invalid_unicast': {
                'type': 'str',
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/cgnv6/l4"

    f_dict = {}

    return url_base.format(**f_dict)


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/cgnv6/l4"

    f_dict = {}

    return url_base.format(**f_dict)


def report_changes(module, result, existing_config, payload):
    change_results = copy.deepcopy(result)
    if not existing_config:
        change_results["modified_values"].update(**payload)
        return change_results

    config_changes = copy.deepcopy(existing_config)
    for k, v in payload["l4"].items():
        v = 1 if str(v).lower() == "true" else v
        v = 0 if str(v).lower() == "false" else v

        if config_changes["l4"].get(k) != v:
            change_results["changed"] = True
            config_changes["l4"][k] = v

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
    payload = utils.build_json("l4", module.params, AVAILABLE_PROPERTIES)
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
                    "acos_info"] = info["l4"] if info != "NotFound" else info
            elif module.params.get("get_type") == "list":
                get_list_result = api_client.get_list(module.client,
                                                      existing_url(module))
                result["axapi_calls"].append(get_list_result)

                info = get_list_result["response_body"]
                result["acos_info"] = info[
                    "l4-list"] if info != "NotFound" else info
            elif module.params.get("get_type") == "stats":
                get_type_result = api_client.get_stats(module.client,
                                                       existing_url(module),
                                                       params=module.params)
                result["axapi_calls"].append(get_type_result)
                info = get_type_result["response_body"]
                result["acos_info"] = info["l4"][
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
