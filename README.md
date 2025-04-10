# Microsoft SCCM

Publisher: Splunk \
Connector Version: 2.3.3 \
Product Vendor: Microsoft \
Product Name: SCCM \
Minimum Product Version: 6.3.0

This app integrates with Microsoft System Center Configuration Manager (SCCM) to execute investigative and generic actions

Windows Remote Management (WinRM) should be enabled on the MS SCCM Server for the app to run
commands remotely. To allow HTTP communication, WinRM config parameter **AllowUnencrypted** should
be changed to true on SCCM server.

By default WinRM HTTP uses port 80. On Windows 7 and higher the default port is 5985.\
By default WinRM HTTPS uses port 443. On Windows 7 and higher the default port is 5986.

The use of the HTTP_PROXY and HTTPS_PROXY environment variables is
currently unsupported.

### Authentication

This app uses different default authorisation method depending on whether FIPS is enabled:
| FIPS | Default auth |
|----------|--------------|
| Enabled | Basic HTTP |
| Disabled | NTLM |

In asset configuration more authentication types can be selected:

- certificate
- credssp
- ntlm
- basic
- kerberos (Currently a Kerberos ticket needs to be initialized outside of pywinrm using the kinit command)

### Certificate Authentication

To authenticate using SSL certificates, select `certificate` authentication in asset configuration method and pass following configuration parameters.

- cert_pem_path - A path to signed certificate file that is trusted by the Windows instance, in PEM format

- cert_key_pem_path - A filepath to key used to generate cert_pem file

- ca_trust_path - The certificate of the certificate authority that signed cert_file. It's needed only when you set up your own certificate authority.

It is recommended that these files be placed under the \<PHANTOM_HOME>/etc/ssl/ directory. These files must be readable by the phantom-worker user.

### Kerberos Authentication

To authenticate using Kerberos, select `kerberos` authentication in asset configuration and provide hostname and username used for authorization.
You'll also need to setup your instance to support Kerberos:

- Kerberos packages have to be installed:

  - for Debian/Ubuntu/etc: `sudo apt-get install krb5-user`
  - for RHEL/CentOS/etc: `sudo yum install krb5-workstation krb5-libs`

- `/etc/krb5.conf` needs to be properly configured for your realm and kdc

- If there is no DNS configuration, `hosts` file will need to have mappings for server with mssccm under same domain as on Windows server

- `kinit` must be run for principal that will be used to connect to msccm

- It should be noted that Kerberos tickets will expire, so it is recommended to use a script to
  run `kinit` periodically to refresh the ticket for the user, alternatively `keytab` file can be created on server and used on client for connectivity.

### Configuration variables

This table lists the configuration variables required to operate Microsoft SCCM. These variables are specified when configuring a SCCM asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**server_url** | required | string | Server URL |
**verify_server_cert** | optional | boolean | Verify server certificate |
**username** | required | string | Username |
**password** | optional | password | Password |
**auth_method** | optional | string | Authentication Method |
**cert_pem_path** | optional | string | Path to SSL certificate PEM file |
**cert_key_pem_path** | optional | string | Path to SSL key file |
**ca_trust_path** | optional | string | Path to trusted CRT file |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[deploy patch](#action-deploy-patch) - Deploy patch \
[list patches](#action-list-patches) - List all software patches \
[list device groups](#action-list-device-groups) - List all device groups

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'deploy patch'

Deploy patch

Type: **generic** \
Read only: **True**

This action will deploy the specified software patch on all the clients belonging to <b>device_group_name</b>. The software patch should be downloaded on the SCCM site server before deploying it.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**software_patch_name** | required | Software Patch Name | string | `sccm software patch name` |
**device_group_name** | required | Device Group Name | string | `sccm device group name` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.device_group_name | string | `sccm device group name` | Test |
action_result.parameter.software_patch_name | string | `sccm software patch name` | Security Update for Microsoft .NET Framework 4.5 on Windows 8 and Windows Server 2012 for x64-based Systems (KB2840632) |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | Patch deployed successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list patches'

List all software patches

Type: **investigate** \
Read only: **True**

Software patches are ordered by software title.

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.ArticleID | string | | 834693 |
action_result.data.\*.BulletinID | string | | |
action_result.data.\*.DatePosted | string | | 05-04-2012 03:21:35 |
action_result.data.\*.DateRevised | string | | 05-04-2012 03:21:35 |
action_result.data.\*.IsDeployed | string | | False |
action_result.data.\*.IsExpired | string | | False |
action_result.data.\*.IsSuperseded | string | | False |
action_result.data.\*.LocalizedDisplayName | string | `sccm software patch name` | Office XP Service Pack 3 for Access 2002 Runtime |
action_result.data.\*.PercentCompliant | string | | 0 |
action_result.summary.total_software_patches | numeric | | 1146 |
action_result.message | string | | Total software patches: 1146 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list device groups'

List all device groups

Type: **investigate** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.CollectionID | string | | SMS00001 |
action_result.data.\*.CollectionRules | string | | Microsoft.ConfigurationManagement.ManagementProvider.IResultObject[] |
action_result.data.\*.CollectionType | string | | 2 |
action_result.data.\*.CollectionVariablesCount | string | | 0 |
action_result.data.\*.Comment | string | | All Systems |
action_result.data.\*.CurrentStatus | string | | 1 |
action_result.data.\*.HasProvisionedMember | string | | True |
action_result.data.\*.ISVData | string | | |
action_result.data.\*.ISVDataSize | string | | 0 |
action_result.data.\*.ISVString | string | | |
action_result.data.\*.IncludeExcludeCollectionsCount | string | | 0 |
action_result.data.\*.IsBuiltIn | string | | True |
action_result.data.\*.IsReferenceCollection | string | | True |
action_result.data.\*.LastChangeTime | string | | 14-09-2017 10:41:40 |
action_result.data.\*.LastMemberChangeTime | string | | 20-09-2017 13:27:47 |
action_result.data.\*.LastRefreshTime | string | | 03-10-2017 22:30:55 |
action_result.data.\*.LimitToCollectionID | string | | |
action_result.data.\*.LimitToCollectionName | string | | |
action_result.data.\*.LocalMemberCount | string | | 3 |
action_result.data.\*.MemberClassName | string | | SMS_CM_RES_COLL_SMS00001 |
action_result.data.\*.MemberCount | string | | 3 |
action_result.data.\*.MonitoringFlags | string | | 0 |
action_result.data.\*.Name | string | `sccm device group name` | All Systems |
action_result.data.\*.ObjectPath | string | | |
action_result.data.\*.OwnedByThisSite | string | | True |
action_result.data.\*.PSComputerName | string | `host name` | SCCMSERVER.sccm.test |
action_result.data.\*.PSShowComputerName | string | | False |
action_result.data.\*.PowerConfigsCount | string | | 0 |
action_result.data.\*.RefreshSchedule | string | | Microsoft.ConfigurationManagement.ManagementProvider.IResultObject[] |
action_result.data.\*.RefreshType | string | | 4 |
action_result.data.\*.ReplicateToSubSites | string | | True |
action_result.data.\*.ServiceWindowsCount | string | | 0 |
action_result.data.\*.SmsProviderObjectPath | string | | SMS_Collection.CollectionID="SMS00001" |
action_result.data.\*.UseCluster | string | | False |
action_result.summary.total_device_groups | numeric | | 5 |
action_result.message | string | | Total device groups: 5 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
