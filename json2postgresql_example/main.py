#!/usr/bin/python
import json
import jsonpath_ng
import psycopg2
from .config import get_config


def get_connection():
    conn = None
    try:
        params = get_config()
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        raise error
    return conn


def insert_interfaces(interfaces):
    """ Insert multiple interface rows.
    """
    sql = ('INSERT INTO interface '
           '(name, description, max_frame_size, config, '
           'port_channel_id) '
           'VALUES(%s, %s, %s, %s, %s)')
    conn = None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, interfaces)


def get_json_data(filename):
    with open(filename) as file:
        return json.loads(file.read())


def get_device_interfaces(filename):
    """ Iterates over device interfaces.
    Yields pair of values: interface group name, interface obj
    """
    json_data = get_json_data(filename)
    paths = [
        "'frinx-uniconfig-topology:configuration'.'Cisco-IOS-XE-native:native'.interface.'Port-channel'",
        "'frinx-uniconfig-topology:configuration'.'Cisco-IOS-XE-native:native'.interface.'TenGigabitEthernet'",
        "'frinx-uniconfig-topology:configuration'.'Cisco-IOS-XE-native:native'.interface.'GigabitEthernet'",
        # "'frinx-uniconfig-topology:configuration'.'Cisco-IOS-XE-native:native'.interface.'BDI'",
        # "'frinx-uniconfig-topology:configuration'.'Cisco-IOS-XE-native:native'.interface.'Loopback'"
        ]
    for path in paths:
        for match in jsonpath_ng.parse(path).find(json_data):
            for intfc in match.value: yield str(match.path), intfc


def format_interface_db(intf_group, intf):
    port_channel = intf.get("Cisco-IOS-XE-ethernet:channel-group", None)
    return ('{}{}'.format(intf_group, intf['name']),
            intf.get('description', None),
            intf.get('mtu', None),
            json.dumps(intf),
            port_channel.get('name', None) if port_channel else None)


def main():
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'configClear_v2.json'

    interfaces = [format_interface_db(intfg, intf) for intfg, intf
                  in get_device_interfaces(filename)]
    insert_interfaces(interfaces)
    print("Added {} interfaces.".format(len(interfaces)))


if __name__ == '__main__':
    main()
