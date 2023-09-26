## **Cisco Backup Configuration using Python3 and CSV**

This script is designed to backup Cisco device configurations for all SIZ DC1 & DC2 machines, by selecting the appropriate option. Each device's parameters are read from a CSV file.

### **Requirements**

Python 3.10
Dependencies: 
All pre-installed libraries except Netmiko. 
Install the dependencies using `pip install -r requirements.txt`

Installation

Clone the repository: `https://github.com/panosnaz/SIZ_DC_config_backup.git`

### **Usage**

- Open the terminal and navigate to the project directory.
- Run the backup.py script using the command python backup.py.
- The script will prompt you to choose the backup option for DC1 routers, DC1 Nexus, DC2 routers, DC2 Nexus, or all devices.
- Based on your selection, the script will read the corresponding CSV file containing the device information and start the backup process for each device.
- If the SSH port (TCP 22) of any device is closed, the script will skip the backup for that device and log the information in a separate file.
- Once the backup process is completed, the script will compress and password-protect the backup files, if the user chooses to do so. It will then ask if you want to open the backup directory or the ZIP file location.


### **Script Files**

- `backup.py`: The main Python script that performs the backup process.
- `requirements.txt`: Contains the list of dependencies required for the script.
- `CSV/DC1_routers.csv, CSV/DC1_nexus.csv, CSV/DC2_routers.csv, CSV/DC2_nexus.csv`: CSV files containing the device information for each category.

### **Additional Notes**

- The script uses Netmiko to connect to Cisco devices via SSH and retrieve the running configuration.
- If the SSH port of any device is closed, the script will skip the backup for that device and log the information in a separate file.
- The backup files are organized in directories based on device categories (DC1_routers, DC1_nexus, DC2_routers, DC2_nexus), and each file is named with the device hostname and the backup date and time.
- After completing the backup process, the script compresses and password-protects the backup files into a ZIP file.
- You can choose to open either the backup directory or the ZIP file location after the backup process.

Notes: 

Make sure to set the correct file paths and credentials in the CSV files before running the script.
Make sure your project structure looks like this:

```
|-- backup.py
|-- CSV/
|   |-- DC1_routers.csv
|   |-- DC1_nexus.csv
|   |-- DC2_routers.csv
|   |-- DC2_nexus.csv
```