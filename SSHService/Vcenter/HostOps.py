__author__ = 'smrutim'
import paramiko
from pyVmomi import vim

from pyVim.connect import SmartConnect, Disconnect
import atexit
import getpass
from logging import error, warning, info, debug
import re
import ssl
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from SSHService.Vcenter import Datacenter
from SSHService.CustomSSH import customssh



def Enable_ESX_Shell(logger,si,hostList):
    content = si.RetrieveContent()
    success_enable_esx_shell = []
    for h in hostList:
        logger.info("THREAD - Enable_ESX_Shell - Enabling ESX Shell on %s"%h)
        host_system = Datacenter.get_obj(content, [vim.HostSystem], h)
        service_system = host_system.configManager.serviceSystem
        esx_shell = [x for x in service_system.serviceInfo.service if x.key == 'TSM'][0]
        try:
            if not esx_shell.running:
                service_system.Start(esx_shell.key)

            service_system.UpdateServicePolicy(esx_shell.key, "on")
            success_enable_esx_shell.append(h)
        except Exception,e:
            logger.error("THREAD - Enable_ESX_Shell - Error while Enabling ESX Shell %s"%str(e))
    return success_enable_esx_shell

def Enable_SSH(logger,si,hostList):
    success_enable_ssh = []
    content = si.RetrieveContent()
    for h in hostList:
        logger.info("THREAD - Enable_SSH - Enabling SSH on %s" % h)
        host_system = Datacenter.get_obj(content, [vim.HostSystem], h)
        service_system = host_system.configManager.serviceSystem
        ssh_service = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
        try:
            if not ssh_service.running:
                service_system.Start(ssh_service.key)
            service_system.UpdateServicePolicy(ssh_service.key, "on")
            success_enable_ssh.append(h)
        except Exception, e:
            logger.error("THREAD - Enable_SSH - Error while Enabling SSH %s" % str(e))
    return success_enable_ssh


def Change_ESX_password(logger,hostList,username,oldpassword,newpassword):
    sucessHostArray = []
    for h in hostList:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logger.info("THREAD - Change_ESX_password - Changing Password.")
            change_esx_pass = "esxcli system account set -i " + username + " -p  " \
                             + newpassword +  " -c " + newpassword
            (ret, stdout, stderr) = customssh.RunCmdOverSSH(change_esx_pass, h, username, oldpassword,timeout=1200)
            print ("THREAD - Change_ESX_password - Password Changed for host %s"%h)
            sucessHostArray.append(h)
        except Exception, e1:
            print "THREAD - Change_ESX_password - The error while changing passowrd for host %s is %s "%(h ,str(e1))

        finally:
            ssh.close()
    if len(sucessHostArray) > 0 :
        return True
    else:
        return False

def Enable_Set_NTP(logger,si,hostList,ntpServers):
    enable_ntp = []
    content = si.RetrieveContent()
    searchIndex = content.searchIndex
    for esxHost in hostList:
        try:
            host = searchIndex.FindByDnsName(dnsName=esxHost, vmSearch=False)
            # NTP manager on ESXi host
            logger.info("THREAD - Enable_Set_NTP - Configuring NTP Server on Host %s"%esxHost)
            dateTimeManager = host.configManager.dateTimeSystem

            # configure NTP Servers if not configured
            ntpConfig = vim.HostNtpConfig(server=ntpServers)
            dateConfig = vim.HostDateTimeConfig(ntpConfig=ntpConfig)
            dateTimeManager.UpdateDateTimeConfig(config=dateConfig)

            # start ntpd service
            serviceManager = host.configManager.serviceSystem
            if dateTimeManager.dateTimeInfo.ntpConfig.server != []:
                logger.info("THREAD - Enable_Set_NTP - Starting ntpd service on " + esxHost)
                serviceManager.StartService(id='ntpd')
                logger.info("THREAD - Enable_Set_NTP - NTP Service started on " + esxHost)
            enable_ntp.append(esxHost)
        except Exception, e:
            print "THREAD - Enable_Set_NTP - Error while configurimg services %s"%str(e)















