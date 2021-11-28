from firepyer import Fdm
from pprint import pprint
import random
import string
import time

# from menu import menu
import ipaddress
import getpass
import json
import sys


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
    hostname = fdm.get_hostname()

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
    dhcp_relay_service_version = dhcp_relay_service["version"]
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
            dhcp_server_interface = interface_choices[int(menu(interface_choices))]
            break
        except (IndexError, ValueError) as e:
            print("Invalid choice, try again")
            continue

    # Where to enable DHCP relay on
    # add all chosen interfaces into the list - need to create an object for each interface
    dhcp_relay_agent_interfaces = []
    print("\nWhat interface-name do you want to enable DHCP relay on?\n")
    while True:
        try:
            dhcp_relay_interface = interface_choices[int(menu(interface_choices))]
            dhcp_relay_agent_interfaces.append(dhcp_relay_interface)
            print(f"\nYou have selected {dhcp_relay_interface['name']}")
            print("Do you need to enable dhcp relay on another interface?")
            loop_choice = input("y/n: ")
            if loop_choice == "y":
                continue
            else:
                break
        except (IndexError, ValueError) as e:
            print("Invalid choice, try again")
            continue

    dhcp_agents = []

    for x in dhcp_relay_agent_interfaces:
        dhcp_agents_object = {}
        # print(x["name"])
        dhcp_agents_object.update(
            {
                "enableIpv4Relay": True,
                "enableIpv6Relay": False,
                "setRoute": True,
                "interface": {"id": x["id"], "type": x["type"]},
                "type": "dhcprelayagent",
            }
        )
        dhcp_agents.append(dhcp_agents_object)
    # print("printing dhcp_agents_object")

    pprint("*" * 100)
    pprint("Your Changes:")
    pprint(
        f"DHCP Relay Server IP: {dhcp_relay_server_ip}, reachabe via {dhcp_server_interface['name']}"
    )
    for x in dhcp_relay_agent_interfaces:
        pprint(f"Enable DHCP Relay on: {x['name']}")

    deploy_to_ftd = input(f"\nDo you want to deploy this to {hostname}? (y/n): ")
    if deploy_to_ftd == "y":

        # create Network object ID, if it exists, compare the value of current ip address vs the input ip address.
        # if it's the same, re-use the same object, else create a new one and append a random 4 digit/string to the end of the object name
        try:
            # create a network object from the IP address.
            dhcp_relay_server_object = fdm.create_network(
                f"{str(dhcp_relay_server_ip)}_dhcp_relay",
                str(dhcp_relay_server_ip),
                "HOST",
            )
        except Exception as e:
            dhcp_relay_server_object = fdm.get_net_objects(
                f"{str(dhcp_relay_server_ip)}_dhcp_relay"
            )
            # if current ip address is the same as the input ip address, re-use the same object
            if dhcp_relay_server_object["value"] == dhcp_relay_server_ip:
                pass
            else:
                dhcp_relay_server_object = fdm.create_network(
                    f"{str(dhcp_relay_server_ip)}_dhcp_relay_new_{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}",
                    str(dhcp_relay_server_ip),
                    "HOST",
                )

        dhcp_relay_server_object_id = dhcp_relay_server_object["id"]

        dhcp_service_payload = {
            "version": dhcp_relay_service_version,
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
                        "id": dhcp_server_interface["id"],
                        "type": dhcp_server_interface["type"],
                    },
                    "type": "dhcprelayserver",
                }
            ],
            "agents": dhcp_agents,
            "id": dhcp_relay_service_id,
            "type": "dhcprelayservice",
        }
        # PUT the payload to the device
        put_dhcp_relay_service = fdm.put_api(
            f"https://{ftd_ip_address}/api/fdm/v6/devicesettings/default/dhcprelayservices/{dhcp_relay_service_id}",
            json.dumps(dhcp_service_payload),
        )
        if (
            put_dhcp_relay_service.status_code == 200
            or put_dhcp_relay_service.status_code == 204
        ):
            print("DHCP relay service created successfully... now deploying.")
        else:
            print("Something went wrong, try again")
            response_error = json.loads(put_dhcp_relay_service.text)
            print(response_error["error"]["messages"][0]["description"])
            sys.exit(1)
        deploy_it = fdm.deploy_now()
        deployment_status = fdm.get_deployment_status(deploy_it)
        deployment_data = ["QUEUED", "DEPLOYING", "DEPLOYED", "FAILED"]
        while deployment_status in deployment_data:
            print(f"Deployment Status: {deployment_status}")
            deployment_status = fdm.get_deployment_status(deploy_it)
            if deployment_status == "DEPLOYED":
                print("Deployment Successful")
                break
            elif deployment_status == "FAILED":
                print("Deployment Failed")
                break
            time.sleep(5)
    elif deploy_to_ftd == "n":
        print("Changes not deployed")
    else:
        print("Invalid choice, try again")
        sys.exit(1)


if __name__ == "__main__":
    main()
