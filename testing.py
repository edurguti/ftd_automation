from pprint import pprint


interface_choices = [
    {
        "hardwareName": "Ethernet1/1",
        "name": "outside",
        "type": "physicalinterface",
        "id": "8d6c41df-3e5f-465b-8e5a-d336b282f93f",
    },
    {
        "hardwareName": "Ethernet1/4",
        "name": "test-name",
        "type": "physicalinterface",
        "id": "d40b7a47-2d9d-11ec-a746-794ec9af0d40",
    },
    {
        "name": "inside",
        "type": "subinterface",
        "id": "842d0445-2dc6-11ec-a746-c5353c179a38",
    },
    {
        "name": "dmz-non-pci",
        "type": "subinterface",
        "id": "8d148701-2dc6-11ec-a746-ef1ce08ad4c0",
    },
    {
        "name": "dmz-workstations",
        "type": "subinterface",
        "id": "9fd3439a-2dc6-11ec-a746-8f5738ea5086",
    },
    {
        "name": "dmz-pci",
        "type": "subinterface",
        "id": "aa721344-2dc6-11ec-a746-478da4297517",
    },
    {
        "name": "dmz-pos-terminal",
        "type": "subinterface",
        "id": "b58e293a-2dc6-11ec-a746-e1a32a382bea",
    },
    {
        "name": "dmz-non-domain",
        "type": "subinterface",
        "id": "ca003b41-2dc6-11ec-a746-110ebb716b0e",
    },
    {
        "name": "dmz-facilities",
        "type": "subinterface",
        "id": "d448d497-2dc6-11ec-a746-69a564f25cf9",
    },
    {
        "name": "dmz-doorlocks",
        "type": "subinterface",
        "id": "3cbe9092-2fe9-11ec-a746-29afc204a5f0",
    },
    {
        "name": "dmz-mgmt",
        "type": "subinterface",
        "id": "f28322d0-30a5-11ec-a746-85857cfcabbf",
    },
    {
        "name": "dmz-3c",
        "type": "subinterface",
        "id": "6c65c801-4817-11ec-8477-0195032cab9a",
    },
]


def menu(options):
    """
    This function will display a menu of options to the user and return the user's choice.
    """
    for option in options:
        print(f"{options.index(option)}: {option}")
    choice = input("Enter your choice: ")
    return choice


agents = {
    "enableIpv4Relay": True,
    "enableIpv6Relay": False,
    "setRoute": True,
    "interface": {
        "version": "daqzbqqfbvj7u",
        "name": "dmz-workstations",
        "hardwareName": "Ethernet1/2.52",
        "id": "9fd3439a-2dc6-11ec-a746-8f5738ea5086",
        "type": "subinterface",
    },
    "type": "dhcprelayagent",
}


dhcp_relay_agent_interfaces = []
while True:
    try:
        dhcp_relay_interface = interface_choices[int(menu(interface_choices))]
        dhcp_relay_agent_interfaces.append(dhcp_relay_interface)
        print(f"\nYou have selected {dhcp_relay_interface['name']}")
        print("Do you need to enable dhcp relay on another interface?")
        yes_no = input("Enter y or n: ")
        if yes_no.lower() == "n":
            break
        if yes_no.lower() == "y":
            continue
        if yes_no.lower() != "y" and yes_no.lower() != "n":
            print("Invalid input")
            continue
    except (IndexError, ValueError) as e:
        print("Invalid choice, try again")
        continue

dhcp_agent_objects = []

# pprint(dhcp_relay_agent_interfaces)
for x in dhcp_relay_agent_interfaces:
    dhcp_object = {}
    dhcp_object.update(
        {
            "enableIpv4Relay": True,
            "enableIpv6Relay": False,
            "setRoute": True,
            "interface": {
                "id": x["id"],
                "type": x["type"],
            },
            "type": "dhcprelayagent",
        }
    )
    dhcp_agent_objects.append(dhcp_object)

pprint(dhcp_agent_objects)
