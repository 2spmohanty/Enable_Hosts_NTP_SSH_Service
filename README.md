# Enable_Hosts_NTP_SSH_Service
This is written in pytest framework. Running it will enable SSH and NTP service in the Hosts of vCenter.

Run this as a pytest to generate Results and failure for Enabling SSH, ESX Shell, and NTP.
The test creates a log file as well as a junit style result xml, that can be feed
in Jenkins for pipeline automation.

Record the changes done, in this section for quick reference.

# Dependency:
pip install pytest
pip install pytest-dependency

# Run:

pytest python -m pytest TestEnableService.py -v -s --junitxml=enableServiceTest.xml

# Input Data 

The input data would be taken from config.py file under Data directory.
Make changes to the input value in the config.py file.

