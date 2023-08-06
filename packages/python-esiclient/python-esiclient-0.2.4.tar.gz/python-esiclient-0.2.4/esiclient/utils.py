#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.


def get_network_display_name(network):
    """Return Neutron network name with vlan, if any

    :param network: a Neutron network
    """
    try:
        return "{0} ({1})".format(
            network.name, network.provider_segmentation_id)
    except Exception:
        # if user does not have permission to see provider_segmentation_id,
        # just show the name
        return network.name


def get_network_info_from_port(port, client, networks_dict={}):
    """Return Neutron network name and ips from port

    :param port: a Neutron port
    :param client: neutron client
    :param networks_dict: networks dict {id:network}
    """
    if port.network_id in networks_dict:
        network = networks_dict.get(port.network_id)
    else:
        network = client.get_network(port.network_id)
    fixed_ip = ''
    if port.fixed_ips and len(port.fixed_ips) > 0:
        fixed_ip = port.fixed_ips[0]['ip_address']

    return get_network_display_name(network), fixed_ip


def get_full_network_info_from_port(port, client, networks_dict={}):
    """Return full Neutron network name and ips from port

    This code iterates through subports if appropriate

    :param port: a Neutron port
    :param client: neutron client
    :param networks_dict: networks dict {id:network}
    """
    network_names = []
    port_names = []
    fixed_ips = []

    network_name, fixed_ip = get_network_info_from_port(port, client,
                                                        networks_dict)
    network_names.append(network_name)
    fixed_ips.append(fixed_ip)
    port_names.append(port.name)

    if port.trunk_details:
        subports = port.trunk_details['sub_ports']
        for subport_info in subports:
            subport = client.get_port(subport_info['port_id'])
            network_name, fixed_ip = get_network_info_from_port(
                subport, client, networks_dict)
            network_names.append(network_name)
            fixed_ips.append(fixed_ip)
            port_names.append(subport.name)

    return network_names, port_names, fixed_ips


def get_port_name(network_name, prefix=None, suffix=None):
    port_name = network_name
    if prefix:
        port_name = "{0}-{1}".format(prefix, port_name)
    if suffix:
        port_name = "{0}-{1}".format(port_name, suffix)
    port_name = "esi-{0}".format(port_name)
    return port_name


def get_or_create_port(port_name, network, client):
    ports = list(client.ports(name=port_name, status='DOWN'))
    if len(ports) > 0:
        port = ports[0]
    else:
        port = client.create_port(
            name=port_name,
            network_id=network.id,
            device_owner='baremetal:none'
        )
    return port


def get_switch_trunk_name(switch, switchport):
    return switch + "-" + switchport


def get_baremetal_port_from_switchport(switch, switchport, ironic_client):
    ports = ironic_client.port.list(detail=True)
    return next((port for port in ports
                 if port.local_link_connection.get(
                         'port_id') == switchport and
                 port.local_link_connection.get(
                     'switch_info') == switch),
                None)


def get_network_from_vlan(vlan_id, neutron_client):
    networks = list(neutron_client.networks(
        provider_network_type='vlan',
        provider_segmentation_id=vlan_id))
    return next(iter(networks), None)


def get_floating_ip(port_id, floating_ips, networks_dict):
    """Return neutron port floating ips information, if any

    :param port_id: Neutron port ID
    :param floating_ips: floating ips list
    :param networks_dict: Neutron networks dict {"id": "name"}
    """
    floating_ip_addresses = [f_ip.floating_ip_address for f_ip in floating_ips
                             if f_ip.port_id == port_id]
    floating_network_ids = [f_ip.floating_network_id for f_ip in floating_ips
                            if f_ip.port_id == port_id]
    floating_network_names = [networks_dict.get(id).name
                              for id in floating_network_ids]
    return floating_ip_addresses, floating_network_names
