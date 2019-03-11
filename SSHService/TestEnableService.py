__author__ = 'smrutim'
import pytest
import time
from pyVmomi import vim
from SSHService.Vcenter import Datacenter,HostOps
from SSHService.Data import config
from SSHService.CustomLogger import CustomLogging

##################################################################################
"""

Run this as a pytest to generate Results and failure for Enabling SSH and ESX Shell.
The test creates a log file as well as a junit style result xml, that can be feed
in Jenkins for pipeline automation.

Record the changes done, in this section for quick reference.

Dependency:
pip install pytest
pip install pytest-dependency

Run:
pytest python -m pytest TestEnableService.py -v -s --junitxml=enableServiceTest.xml

Enables NTP and SSH Service


version 1 :
Initial : Author : smrutim
"""
#####################################################################################

#Create Logger for the Test
logger = CustomLogging.generate_logger(log_file=config.LOG_FILE_NAME)

#Login to VC
@pytest.mark.dependency()
def test_Login():
    pytest.si = Datacenter.Login(logger,config.VCENTER,config.VCENTER_USER,config.VCENTER_PASSWORD)
    assert pytest.si is not None, "Getting connect Anchor to VC not successful."



@pytest.mark.dependency(depends=["test_Login"])
def test_Enable_ESX_Shell():
    enable_esxi_shell = HostOps.Enable_ESX_Shell(logger,pytest.si,config.HOST_LIST)
    assert len(enable_esxi_shell) > 0 , "ESXI shell couldnot be enabled on any Hosts."



@pytest.mark.dependency(depends=["test_Login"])
def test_Enable_SSH():
    enable_ssh = HostOps.Enable_SSH(logger, pytest.si, config.HOST_LIST)
    assert len(enable_ssh) > 0, "SSH couldnot be enabled on any Hosts."


@pytest.mark.dependency(depends=["test_Login","test_Enable_SSH"])
def test_Change_ESX_password():
    change_ssh_pass = HostOps.Change_ESX_password(logger,config.HOST_LIST,config.ROOT_USER,
                                                  config.OLD_ROOT_PASSWORD,config.NEW_ROOT_PASSWORD)
    assert change_ssh_pass, "Root password can't be changed for any hosts."


@pytest.mark.dependency(depends=["test_Login"])
def test_Enable_Set_NTP():
    enable_ntp = HostOps.Enable_Set_NTP(logger,pytest.si,config.HOST_LIST,config.NTP_SERVER)
    assert len(enable_ntp) > 0, "NTP Service couldnot be enabled on any Hosts."























