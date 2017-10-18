# --
# File: microsoftsccm_consts.py
#
# Copyright (c) Phantom Cyber Corporation, 2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --
MSSCCM_CONFIG_SERVER_URL = "server_url"
MSSCCM_CONFIG_USERNAME = "username"
MSSCCM_CONFIG_PASSWORD = "password"
MSSCCM_CONFIG_VERIFY_SSL = "verify_server_cert"
MSSCCM_SERVER_URL = "{url}/wsman"
MSSCCM_CONNECTING_ENDPOINT_MSG = "Connecting to endpoint"
MSSCCM_ERR_SERVER_CONNECTION = "Connection failed"
MSSCCM_ERR_BAD_HANDSHAKE = "Bad Handshake"
MSSCCM_INVALID_CREDENTIAL_ERR = "Invalid Credentials"
MSSCCM_EXCEPTION_OCCURRED = "Exception occurred"
MSSCCM_TEST_CONNECTIVITY_FAIL = "Test Connectivity Failed."
MSSCCM_TEST_CONNECTIVITY_PASS = "Test Connectivity Passed"
MSSCCM_PS_COMMAND = 'powershell -command "{command}"'
MSSCCM_JSON_FORMAT_ERROR = "JSON format error"
MSSCCM_PARAM_SF_UPDATE_NAME = "software_update_name"
MSSCCM_PARAM_COLLECTION_NAME = "collection_name"
MSSCCM_GET_SOFTWARE_UPDATES = 'powershell -command "Import-Module ' \
                              '($Env:SMS_ADMIN_UI_PATH.Substring(0,$Env:SMS_ADMIN_UI_PATH.Length-5)' \
                              ' + {q}\ConfigurationManager.psd1{q});$PSD = Get-PSDrive -PSProvider ' \
                              'CMSite;CD {q}$($PSD):{q};Get-CMSoftwareUpdate -Fast | Select-Object -Property ' \
                              'ArticleID, LocalizedDisplayName, BulletinID, PercentCompliant, IsDeployed, DatePosted,' \
                              ' DateRevised, IsSuperseded, IsExpired | ConvertTo-Csv | ConvertFrom-Csv | ' \
                              'ConvertTo-Json;"'
MSSCCM_INSTALL_SOFTWARE_UPDATES = 'powershell -command " ' \
                                  'Import-Module ($Env:SMS_ADMIN_UI_PATH.Substring(0,$Env:SMS_ADMIN_UI_PATH.Length-5)' \
                                  ' + {q}\ConfigurationManager.psd1{q});$PSD = ' \
                                  'Get-PSDrive -PSProvider CMSite;CD {q}$($PSD):{q}; Start-CMSoftwareUpdateDeployment' \
                                  ' -SoftwareUpdateName {q}{name}{q} -CollectionName {q}{collection_name}{q} ' \
                                  '-DeploymentType Required -VerbosityLevel AllMessages -TimeBasedOn LocalTime ' \
                                  '-UserNotification DisplaySoftwareCenterOnly -ProtectedType RemoteDistributionPoint' \
                                  ' -UnprotectedType UnprotectedDistributionPoint -GenerateSuccessAlert $True' \
                                  ' -DisableOperationsManagerAlert $True -GenerateOperationsManagerAlert $True' \
                                  ' -AcceptEula ;"'
MSSCCM_GET_DEVICE_COLLECTION = 'powershell -command "Import-Module ' \
                               '($Env:SMS_ADMIN_UI_PATH.Substring(0,$Env:SMS_ADMIN_UI_PATH.Length-5) + ' \
                               '{q}\ConfigurationManager.psd1{q}); ' \
                               '$PSD = Get-PSDrive -PSProvider' \
                               ' CMSite;CD {q}$($PSD):{q};Get-CMDeviceCollection | ConvertTo-Csv | ConvertFrom-Csv | ' \
                               'ConvertTo-Json;"'
