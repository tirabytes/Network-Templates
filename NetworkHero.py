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

    # Prompt user for the command to execute
    command = input("Enter the command you want to execute: ")
    
    # Initialize progress bar for command execution
    with tqdm(total=100, desc="Executing Command") as pbar:
        output += net_connect.send_command(command)
        pbar.update(50)  # Update progress bar
        
        # Extract the hostname of the switch
        hostname = net_connect.find_prompt().strip()

        # Get the current date and time
        current_time = datetime.now().strftime("%H-%M-%S")
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Generate filename with hostname, date, and time
        filename = f"{hostname}_{current_date}_{current_time}.txt"

        # Save the output to a text file with hostname, date, and time in the filename
        print("Saving output to file...")
        with open(filename, 'w') as file:
            file.write(output)
        
        pbar.update(50)  # Update progress bar

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

    