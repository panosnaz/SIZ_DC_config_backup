
# ---------------------------------------------------------------------------------------
#
#            Cisco backup configuration using Python3 and CSV
#
# script:                   backup.py
# Install dependencies:     pip install -r requirements.txt
#
# Version: Python 3.10
# Description:   This script is designed to backup cisco device configurations 
#                for all SIZ DC1 & DC2 machines, by selecting the appropriate option.
#                Each device parameters are read from a CSV file.            
#
#  https://github.com/panosnaz/SIZ_DC_config_backup.git
# ---------------------------------------------------------------------------------------

# Libraries
# # All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping 
import os
from termcolor import cprint
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import socket
import shutil
import pyzipper
from config import zip_password

os.system('cls') # Clears the console screen

# Current time and formats it to "Day/Month/Year__Time".
today = datetime.now()
dt_string = today.strftime("%d-%m-%Y__%H-%M")

dir = ("backup_" + today.strftime('%d-%m-%Y'))
DC1_routers_dir = os.path.join((dir),"DC1_routers")
DC1_nexus_dir = os.path.join((dir),"DC1_nexus")
DC2_routers_dir = os.path.join((dir),"DC2_routers")
DC2_nexus_dir = os.path.join((dir),"DC2_nexus")
backup_dir = os.path.join(os.getcwd(),(dir))

def compress_and_encrypt_output_folder():
    global zip_file_path

    """Compresses and password-protects the entire output folder and contents.

    Returns:
        None
    """
    # Ask for user's approval for compression and encryption
    approval = input("Do you want to compress and encrypt the backup folder? [y/N]: ").lower()
    if approval == "y":
    
        output_folder = backup_dir
        zip_file_name = os.path.join(os.getcwd(), f"backup_{dt_string}.zip")

        # Create a password for the ZIP file
        #password = input("Enter the password for the ZIP file: ").encode()

        # Change the current working directory to the parent directory of the output_folder
        # to avoid creating any intermediate directories in the ZIP file
        with pyzipper.AESZipFile(zip_file_name, "w", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zip_file:
            zip_file.setpassword(zip_password)

            # Compress the output folder and add it to the ZIP file
            for root, _, files in os.walk(output_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, output_folder))

        cprint(f"Password-protected ZIP file '{zip_file_name}' created successfully.","yellow")
        cprint(f"Protected with the SIZ admin password","yellow")
        zip_file_path = zip_file_name

    else:
            # If the user does not want to encrypt, set the zip_file_path to None
            cprint("Backup folder compression and encryption skipped.","yellow")
            zip_file_path = None

def test_ssh_port(ip_address, port=22, count=2):
    """
    Test if port TCP 22 (SSH) is open on a remote device.

    Parameters:
        ip_address (str): The IP address of the remote device.
        port (int): The port number to test (default is 22 for SSH).
        count (int): Number of connection attempts to make (default is 2).

    Returns:
        bool: True if the port is open, False otherwise.
    """
    for _ in range(count):
        try:
            with socket.create_connection((ip_address, port), timeout=5):
                return True
        except Exception:
            pass

    return False

# Gives us the information we need to connect.
def get_saved_config_1(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | i uptime")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "__" + dt_string
    # Creates the text file in the backup folder with the special name, and writes to it.
    backupFile = (fileName + ".txt")
    os.makedirs(DC1_routers_dir, exist_ok=True)
    dir1_path = os.path.join(DC1_routers_dir, backupFile)
    file1 = open(dir1_path, "w")
    file1.write(output)

    cprint("-----> " + fileName + ".txt","cyan")


def get_saved_config_2(host, username, password, enable_secret):
    cisco_nxos = {
        'device_type': 'cisco_nxos',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_nxos)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Finds the hostname from the prompt name, and use it for the output file name.
    find_hostname = net_connect.find_prompt()
    hostname = find_hostname.replace("#","")
    
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "__" + dt_string
    # Creates the text file in the backup folder with the special name, and writes to it.
    backupFile = (fileName + ".txt")
    os.makedirs(DC1_nexus_dir, exist_ok=True)
    dir2_path = os.path.join(DC1_nexus_dir, backupFile)
    file2 = open(dir2_path, "w")
    file2.write(output)
    
    cprint("-----> " + fileName + ".txt","cyan")
    

def get_saved_config_3(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | i uptime")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "__" + dt_string
    # Creates the text file in the backup folder with the special name, and writes to it.
    backupFile = (fileName + ".txt")
    os.makedirs(DC2_routers_dir, exist_ok=True)
    dir3_path = os.path.join(DC2_routers_dir, backupFile)
    file3 = open(dir3_path, "w")
    file3.write(output)

    cprint("-----> " + fileName + ".txt","cyan")
    

def get_saved_config_4(host, username, password, enable_secret):
    cisco_nxos = {
        'device_type': 'cisco_nxos',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_nxos)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Finds the hostname from the prompt name, and use it for the output file name.
    find_hostname = net_connect.find_prompt()
    hostname = find_hostname.replace("#","")
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "__" + dt_string
    # Creates the text file in the backup folder with the special name, and writes to it.
    backupFile = (fileName + ".txt")
    os.makedirs(DC2_nexus_dir, exist_ok=True)
    dir4_path = os.path.join(DC2_nexus_dir, backupFile)
    file4 = open(dir4_path, "w")
    file4.write(output)

    cprint("-----> " + fileName + ".txt","cyan")
    
    
# reads the CSV files
"""
The csv_option function iterates over each row in the CSV file, and for each device, 
it performs the following steps:

- It calls the test_ssh_port() function to check if port TCP 22 (SSH) is open on the remote device.
- If the port is open, it proceeds to call the get_saved_config() function to log in to the device and take the backup.
- If the port is closed, it skips the backup process for that device and prints a message indicating that the SSH port is closed.
"""
def csv_option_1():
    
    with open('CSV/DC1_routers.csv') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            host = list_of_rows[rows][4]
            ip = list_of_rows[rows][0]

            # Test if TCP port 22 (SSH) is open on each device
            if test_ssh_port(ip, port=22, count=2):
                # If port is open, proceed with backup
                get_saved_config_1(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
            else:
                # If port is closed, skip backup and print a message
                fileName = "downDevices_" + str(host) + "_" + str(ip) + "_" + dt_string + ".txt"
                downDeviceOutput = open("DC1_routers/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "_" + str(host) + "\n")
                print(str(ip) + " SSH port is closed. Skipping backup.")
                   
def csv_option_2():
    
    with open('CSV/DC1_nexus.csv') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            host = list_of_rows[rows][4]
            ip = list_of_rows[rows][0]
            
            # Test if TCP port 22 (SSH) is open on each device
            if test_ssh_port(ip, port=22, count=2):
                # If port is open, proceed with backup
                get_saved_config_2(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
            else:
                # If port is closed, skip backup and print a message
                fileName = "downDevices_" + str(host) + "_" + str(ip) + "_" + dt_string + ".txt"
                downDeviceOutput = open("DC1_nexus/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "_" + str(host) + "\n")
                print(str(ip) + " SSH port is closed. Skipping backup.")

def csv_option_3():
    
    with open('CSV/DC2_routers.csv') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            host = list_of_rows[rows][4]
            ip = list_of_rows[rows][0]
            
            # Test if TCP port 22 (SSH) is open on each device
            if test_ssh_port(ip, port=22, count=2):
                # If port is open, proceed with backup
                get_saved_config_3(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
            else:
                # If port is closed, skip backup and print a message
                fileName = "downDevices_" + str(host) + "_" + str(ip) + "_" + dt_string + ".txt"
                downDeviceOutput = open("DC2_routers/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "_" + str(host) + "\n")
                print(str(ip) + " SSH port is closed. Skipping backup.")
                         
def csv_option_4():
    
    with open('CSV/DC2_nexus.csv') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            host = list_of_rows[rows][4]
            ip = list_of_rows[rows][0]
            
            # Test if TCP port 22 (SSH) is open on each device
            if test_ssh_port(ip, port=22, count=2):
                # If port is open, proceed with backup
                get_saved_config_4(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
            else:
                # If port is closed, skip backup and print a message
                fileName = "downDevices_" + str(host) + "_" + str(ip) + "_" + dt_string + ".txt"
                downDeviceOutput = open("DC2_nexus/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "_" + str(host) + "\n")
                print(str(ip) + " SSH port is closed. Skipping backup.")

def csv_option_5():
    # Perform backup for all DC1 routers
    cprint("Backing up DC1 routers...", "yellow")
    csv_option_1()

    # Perform backup for all DC1 Nexus devices
    cprint("\nBacking up DC1 Nexus devices...", "yellow")
    csv_option_2()

    # Perform backup for all DC2 routers
    cprint("\nBacking up DC2 routers...", "yellow")
    csv_option_3()

    # Perform backup for all DC2 Nexus devices
    cprint("\nBacking up DC2 Nexus devices...", "yellow")
    csv_option_4()

def ask_for_option():

# Ask the user what option they are going to use, keep asking until a valid option is chosen.
    while True:
        cprint("\n1. Backup DC1 routers.","yellow")
        cprint("2. Backup DC1 nexus.","yellow")
        cprint("3. Backup DC2 routers.","yellow")
        cprint("4. Backup DC2 nexus.","yellow")
        cprint("5. Backup ALL devices.\n", "yellow")
        choice = input("Please pick an option: ")

        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        else:
            print("Invalid option. Please choose one of the backup options.")

# Ask for user's choice
selected_option = ask_for_option()

# This list will store all the backup directories created during the backup process.
backup_dirs = []

# This basically runs the whole file.
if selected_option == "1":
    csv_option_1()
    backup_dirs.append(DC1_routers_dir)
elif selected_option  == "2":
    csv_option_2()
    backup_dirs.append(DC1_nexus_dir)
elif selected_option  == "3":
    csv_option_3()
    backup_dirs.append(DC2_routers_dir)
elif selected_option  == "4":
    csv_option_4()
    backup_dirs.append(DC2_nexus_dir)
elif selected_option == "5":
    csv_option_5()
    backup_dirs.append(DC1_routers_dir)
    backup_dirs.append(DC1_nexus_dir)
    backup_dirs.append(DC2_routers_dir)
    backup_dirs.append(DC2_nexus_dir)

# Perform compression and encryption after all backup operations
compress_and_encrypt_output_folder()

# Remove the temporary backup directory only if it was compressed and encrypted successfully
if zip_file_path is not None:
    shutil.rmtree(backup_dir)

# Ask to open the backup directory or ZIP location based on user selection
if zip_file_path is None:
    decision = (input("Do you want to open the backup directory now? [y/N]: ") or "n").lower()
    if decision == "y":
        os.startfile(dir)
    else:
        cprint(f"INFO: Files are created under below directory:", "grey")
        cprint(backup_dir, "grey", attrs=["bold"])
else:
    decision = (input("Do you want to open the ZIP file location now? [y/N]: ") or "n").lower()
    if decision == "y":
        os.startfile(os.path.dirname(zip_file_path))
    else:
        cprint(f"INFO: Files are created under below directory:", "grey")
        cprint(backup_dir, "grey", attrs=["bold"])


#exec(open('sharepoint_upload.py').read()) 