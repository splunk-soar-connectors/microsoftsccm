# --
# File: microsoftsccm_consts.py
# Copyright (c) 2017-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
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
MSSCCM_TRANSPORT_ERR = "Connection error: Bad configuration in SCCM"
MSSCCM_EXCEPTION_OCCURRED = "Exception occurred"
MSSCCM_TEST_CONNECTIVITY_FAIL = "Test Connectivity Failed."
MSSCCM_TEST_CONNECTIVITY_PASS = "Test Connectivity Passed"
MSSCCM_PS_COMMAND = 'powershell -command "{command}"'
MSSCCM_JSON_FORMAT_ERROR = "JSON format error"
MSSCCM_PARAM_PATCH_NAME = "software_patch_name"
MSSCCM_PARAM_DEVICE_GROUP_NAME = "device_group_name"
MSSCCM_GET_SOFTWARE_PATCHES = 'powershell -command "Import-Module ' \
                              '($Env:SMS_ADMIN_UI_PATH.Substring(0,$Env:SMS_ADMIN_UI_PATH.Length-5)' \
                              ' + {q}\\ConfigurationManager.psd1{q});$PSD = Get-PSDrive -PSProvider ' \
                              'CMSite;CD {q}$($PSD):{q};Get-CMSoftwareUpdate -Fast | Select-Object -Property ' \
                              'ArticleID, LocalizedDisplayName, BulletinID, PercentCompliant, IsDeployed, DatePosted,' \
                              ' DateRevised, IsSuperseded, IsExpired | ConvertTo-Csv | ConvertFrom-Csv | ' \
                              'ConvertTo-Json;"'
MSSCCM_DEPLOY_SOFTWARE_PATCHES = 'powershell -command " ' \
                                  'Import-Module ($Env:SMS_ADMIN_UI_PATH.Substring(0,$Env:SMS_ADMIN_UI_PATH.Length-5)' \
                                  ' + {q}\\ConfigurationManager.psd1{q});$PSD = ' \
                                  'Get-PSDrive -PSProvider CMSite;CD {q}$($PSD):{q}; Start-CMSoftwareUpdateDeployment' \
                                  ' -SoftwareUpdateName {q}{name}{q} -CollectionName {q}{device_group_name}{q} ' \
                                  '-DeploymentType Required -VerbosityLevel AllMessages -TimeBasedOn LocalTime ' \
                                  '-UserNotification DisplaySoftwareCenterOnly -ProtectedType RemoteDistributionPoint' \
                                  ' -UnprotectedType UnprotectedDistributionPoint -GenerateSuccessAlert $True' \
                                  ' -DisableOperationsManagerAlert $True -GenerateOperationsManagerAlert $True' \
                                  ' -AcceptEula ;"'
MSSCCM_GET_DEVICE_GROUPS = 'powershell -command "Import-Module ' \
                               '($Env:SMS_ADMIN_UI_PATH.Substring(0,$Env:SMS_ADMIN_UI_PATH.Length-5) + ' \
                               '{q}\\ConfigurationManager.psd1{q}); ' \
                               '$PSD = Get-PSDrive -PSProvider' \
                               ' CMSite;CD {q}$($PSD):{q};Get-CMDeviceCollection | ConvertTo-Csv | ConvertFrom-Csv | ' \
                               'ConvertTo-Json;"'
