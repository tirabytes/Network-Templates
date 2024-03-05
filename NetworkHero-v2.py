from netmiko import ConnectHandler
from datetime import datetime
from tqdm import tqdm
import time

try:
    # Prompt user for switch details
    host = input("Enter the IP address of the switch: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Define the switch details
    switch = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
    }

    # Establish SSH connection to the switch
    print("Establishing SSH connection...")
    net_connect = ConnectHandler(**switch)
    time.sleep(2)  # Simulating connection time

    # Enter privileged EXEC mode without an enable password
    print("Entering enable mode...")
    net_connect.enable()
    time.sleep(1)  # Simulating enable mode entry

    # Send command with paging disabled to avoid "--- More ---" prompts
    print("Retrieving output...")
    output = net_connect.send_command("terminal length 0")

    # List of predefined commands to execute
    commands = [
        "show running-config",
        "show arp",
        "show ip arp",
        "show mac address-table",
        "show ip route detail",
        "show interface brief",
        # "show interface",
        "show version",
        "show lldp neighbours",
        "show snmp",
        "show logging"
    ]

    combined_output = ""  # Initialize combined output variable

    with tqdm(total=len(commands)*100, desc="Executing Commands") as pbar:
        for command in commands:
            try:
                pbar.set_description(f"Executing Command: {command}")
                if command == "show interface":
                    command_output = net_connect.send_command(command, delay_factor=4)
                else:
                    command_output = net_connect.send_command(command)
                combined_output += f"Command: {command}\n{command_output}\n\n"  # Add command before output with line breaks
            except Exception as e:
                print(f"Command '{command}' failed with error: {e}")
            pbar.update(100)  # Update progress bar for each command

        # Extract the hostname of the switch
        hostname = net_connect.find_prompt().strip()

        # Get the current date and time
        current_time = datetime.now().strftime("%H-%M-%S")
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Generate filename with hostname, date, and time
        filename = f"{hostname}_{current_date}_{current_time}.txt"

        # Save the combined output to a text file with hostname, date, and time in the filename
        print("Saving output to file...")
        with open(filename, 'w') as file:
            file.write(combined_output)
            pbar.update(100)  # Update progress bar for saving output

except Exception as e:
    print(f"An error occurred: {e}")

else:
    print("Script executed successfully.")

finally:
    try:
        net_connect.disconnect()
        print("SSH connection closed.")
    except NameError:
        print("SSH connection was not established.")