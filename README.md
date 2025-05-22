# FTD DHCP Relay Configuration Script

This script automates the configuration of DHCP relay services on Cisco Firepower Threat Defense (FTD) devices.

## Prerequisites

To use this script, you will need the following:

*   **Python 3.8+:** The script utilizes features such as the walrus operator (:=) which was introduced in Python 3.8.
*   **`firepyer` Library:** This Python library is used to interact with the Cisco FTD REST API. Install it using pip:
    ```bash
    pip install firepyer
    ```
*   **Network Connectivity:** Ensure your machine has network connectivity to the management interface of the FTD device you intend to configure.
*   **FTD Credentials:** You'll need a username and password for an FTD account that has permissions to make changes via the REST API.

## How to Run the Script

There are two ways to run this script:

### Local Execution

1.  **Clone or Download the Script:** Obtain a copy of the `create_dhcp_relay.py` script onto your local machine.
2.  **Run the Script:** Open your terminal or command prompt, navigate to the directory where you saved the script, and execute it using:
    ```bash
    python create_dhcp_relay.py
    ```
3.  **Follow Prompts:** The script will then prompt you to enter the necessary information to configure DHCP relay.

### Docker Execution

1.  **Run the Docker Container:** If you have Docker installed, you can run the script using the pre-built Docker image:
    ```bash
    docker run -it edondurguti/ftd_create_dhcp_relay
    ```
2.  **Follow Prompts:** Similar to local execution, the script running inside the Docker container will prompt you for the required information.

## Information Prompts

The script will ask for the following details:

*   **FTD Device IP Address:** The IP address of your FTD's management interface.
*   **FTD Username:** Your username for accessing the FTD device.
*   **FTD Password:** Your password for the FTD device.
*   **DHCP Server IP Address:** The IP address of your DHCP server.
*   **Interface for DHCP Server:** The name of the FTD interface through which the DHCP server is reachable (e.g., `inside`, `DMZ`).
*   **Relay Interfaces:** A comma-separated list of FTD interface names on which you want to enable DHCP relay (e.g., `guest_vlan10,iot_vlan20`).

## How it Works

This script leverages the `firepyer` Python library to communicate with the Cisco FTD's REST API. The automation process involves these steps:

1.  **Connect to FTD:** Establishes a connection to the specified FTD device using the provided credentials.
2.  **Gather Interface Information:** Retrieves details about the FTD's network interfaces to validate user input.
3.  **Create Network Objects:** Checks if network objects for the DHCP server IP and relevant interface IPs already exist. If not, it creates them.
4.  **Configure DHCP Relay:** Sets up the DHCP relay service on the FTD, associating the specified DHCP server with the designated relay interfaces.
5.  **Deploy Changes:** Commits and deploys the configuration changes to the FTD device.

## Disclaimer

*   This script is provided "as-is" without any warranties.
*   It is highly recommended that you understand the script's operations and potential impact before running it on production FTD devices.
*   You are solely responsible for any changes made to your FTD configuration by this script. Always ensure you have backups and a rollback plan.
