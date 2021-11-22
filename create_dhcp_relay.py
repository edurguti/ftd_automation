from firepyer import Fdm
from pprint import pprint

# from menu import menu
import ipaddress
import getpass
import json


def menu(options):
    """
    This function will display a menu of options to the user and return the user's choice.
    """
    for option in options:
        print(f"{options.index(option)}: {option}")
    choice = input("Enter your choice: ")
    return choice


def main():
    while True:
        try:
            ftd_ip_address = ipaddress.ip_address(
                input("Enter IP address of the FTD device (accessible via API/http): ")
            )
            break
        except ValueError:
            print("Invalid IP address")
            continue

    ftd_username = input("Enter username: ")
    ftd_password = getpass.getpass("Enter password: ")

    fdm = Fdm(
        host=ftd_ip_address, username=ftd_username, password=ftd_password, verify=False
    )

    while True:
        try:
            dhcp_relay_server_ip = ipaddress.ip_address(
                input("Enter IP address of the DHCP Server: ")
            )
            break
        except ValueError:
            print("Invalid IP address")
            continue

    dhcp_relay_service = fdm.get_api_single_item(
        "devicesettings/default/dhcprelayservices"
    )
    dhcp_relay_service_id = dhcp_relay_service["id"]
    interface_choices = []
    get_physical_intefaces = fdm.get_interfaces()
    physical_interfaces = []
    for x in get_physical_intefaces:
        physical_interfaces.append(x["hardwareName"])
        if x["name"] != "":
            interface_choices.append(
                {
                    "hardwareName": x["hardwareName"],
                    "name": x["name"],
                    "type": x["type"],
                    "id": x["id"],
                }
            )

    # append all interfaces that have 'name' other than empty "" to the choice list
    for x in physical_interfaces:
        get_sub_interfaces = fdm.get_subinterfaces(x)
        for y in get_sub_interfaces:
            if y["name"] != "":
                interface_choices.append(
                    {
                        "name": y["name"],
                        "type": y["type"],
                        "id": y["id"],
                    }
                )

    print(f"\nWhat interface is  {dhcp_relay_server_ip} reachable from?\n")
    # get route via cli
    show_route = fdm.send_command(f"show route {dhcp_relay_server_ip}")
    print(f"Hint:\n {show_route}")
    while True:
        try:
            choices = interface_choices[int(menu(interface_choices))]
            break
        except (IndexError, ValueError) as e:
            print("Invalid choice, try again")
            continue

    # Where to enable DHCP relay on
    print("\nWhat interface-name do you want to enable DHCP relay on?\n")
    while True:
        try:
            dhcp_relay_choices = interface_choices[int(menu(interface_choices))]
            break
        except (IndexError, ValueError) as e:
            print("Invalid choice, try again")
            continue
    dhcp_relay_server_object = fdm.create_network(
        f"{str(dhcp_relay_server_ip)}_dhcp_relay", str(dhcp_relay_server_ip), "HOST"
    )
    dhcp_relay_server_object_id = dhcp_relay_server_object["id"]
    dhcp_service_payload = {
        # "version": dhcp_relay_service_version,
        "name": "dhcp_relay_1",
        "ipv4RelayTimeout": 60,
        "ipv6RelayTimeout": 60,
        "servers": [
            {
                "server": {
                    "id": dhcp_relay_server_object_id,
                    "type": "networkobject",
                },
                "interface": {
                    "id": choices["id"],
                    "type": choices["type"],
                },
                "type": "dhcprelayserver",
            }
        ],
        "agents": [
            {
                "enableIpv4Relay": True,
                "enableIpv6Relay": False,
                "setRoute": True,
                "interface": {
                    "id": dhcp_relay_choices["id"],
                    "type": dhcp_relay_choices["type"],
                },
                "type": "dhcprelayagent",
            }
        ],
        "id": dhcp_relay_service_id,
        "type": "dhcprelayservice",
    }

    put_dhcp_relay_service = fdm.put_api(
        f"https://{ftd_ip_address}/api/fdm/v6/devicesettings/default/dhcprelayservices/{dhcp_relay_service_id}",
        json.dumps(dhcp_service_payload),
    )

    print(put_dhcp_relay_service.text)

    pprint(put_dhcp_relay_service)


if __name__ == "__main__":
    main()
