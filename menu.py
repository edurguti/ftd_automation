# build an option menu with a list of options from user input


interface_choices = [
    "Ethernet1/4",
    "Ethernet1/2",
    "Ethernet1/3",
    "Management1/1",
    "Ethernet1/1",
    "Ethernet1/8",
    "Ethernet1/7",
    "Ethernet1/11",
    "Ethernet1/10",
    "Ethernet1/9",
]


def menu(options):
    """
    This function will display a menu of options to the user and return the user's choice.
    """
    for option in options:
        print(f"{options.index(option)}: {option}")
    choice = input("Enter your choice: ")
    return choice


# while True:
#     try:
#         choice = my_interface[int(menu(my_interface))]
#     except IndexError:
#         print("Invalid choice, try again")
#         continue

# try:
#     print(my_interface[int(menu(my_interface))])
# except IndexError:
#     print("Invalid choice, try again")
#     print(my_interface[int(menu(my_interface))])
# print(choice)


if __name__ == "__main__":
    while True:
        try:
            dhcp_relay_choices = interface_choices[int(menu(interface_choices))]
            break
        except IndexError:
            print("Invalid choice, try again")
            continue
