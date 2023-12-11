# File: microsoftsccm_consts.py
#
# Copyright (c) 2017-2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
MSSCCM_CONFIG_SERVER_URL = "server_url"
MSSCCM_CONFIG_USERNAME = "username"
MSSCCM_CONFIG_PASSWORD = "password"  # pragma: allowlist secret
MSSCCM_CONFIG_AUTH_METHOD = "auth_method"
MSSCCM_CONFIG_VERIFY_SSL = "verify_server_cert"

MSSCCM_DEFAULT_AUTH_METHOD = "default"

MSSCCM_SERVER_URL = "{url}/wsman"
MSSCCM_CONNECTING_ENDPOINT_MSG = "Connecting to endpoint"
MSSCCM_ERROR_SERVER_CONNECTION = "Connection failed"
MSSCCM_ERROR_BAD_HANDSHAKE = "Bad Handshake"
MSSCCM_INVALID_CREDENTIAL_ERROR = "Invalid Credentials"
MSSCCM_TRANSPORT_ERROR = "Connection error: Bad configuration in SCCM"
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
