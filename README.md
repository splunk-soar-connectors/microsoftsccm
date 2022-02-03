[comment]: # "Auto-generated SOAR connector documentation"
# Microsoft SCCM

Publisher: Splunk  
Connector Version: 2\.1\.2  
Product Vendor: Microsoft  
Product Name: SCCM  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app integrates with Microsoft System Center Configuration Manager \(SCCM\) to execute investigative and generic actions

[comment]: # "    File: README.md"
[comment]: # "  Copyright (c) 2017-2022 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
Windows Remote Management (WinRM) should be enabled on the MS SCCM Server for the app to run
commands remotely. To allow HTTP communication, WinRM config parameter **AllowUnencrypted** should
be changed to true on SCCM server.

By default WinRM HTTP uses port 80. On Windows 7 and higher the default port is 5985.  
By default WinRM HTTPS uses port 443. On Windows 7 and higher the default port is 5986.

This app uses NTLM authorization. The use of the HTTP_PROXY and HTTPS_PROXY environment variables is
currently unsupported.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a SCCM asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**server\_url** |  required  | string | Server URL
**verify\_server\_cert** |  optional  | boolean | Verify server certificate
**username** |  required  | string | Username
**password** |  required  | password | Password

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[deploy patch](#action-deploy-patch) - Deploy patch  
[list patches](#action-list-patches) - List all software patches  
[list device groups](#action-list-device-groups) - List all device groups  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'deploy patch'
Deploy patch

Type: **generic**  
Read only: **True**

This action will deploy the specified software patch on all the clients belonging to <b>device\_group\_name</b>\. The software patch should be downloaded on the SCCM site server before deploying it\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**software\_patch\_name** |  required  | Software Patch Name | string |  `sccm software patch name` 
**device\_group\_name** |  required  | Device Group Name | string |  `sccm device group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.device\_group\_name | string |  `sccm device group name` 
action\_result\.parameter\.software\_patch\_name | string |  `sccm software patch name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list patches'
List all software patches

Type: **investigate**  
Read only: **True**

Software patches are ordered by software title\.

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.ArticleID | string | 
action\_result\.data\.\*\.BulletinID | string | 
action\_result\.data\.\*\.DatePosted | string | 
action\_result\.data\.\*\.DateRevised | string | 
action\_result\.data\.\*\.IsDeployed | string | 
action\_result\.data\.\*\.IsExpired | string | 
action\_result\.data\.\*\.IsSuperseded | string | 
action\_result\.data\.\*\.LocalizedDisplayName | string |  `sccm software patch name` 
action\_result\.data\.\*\.PercentCompliant | string | 
action\_result\.summary\.total\_software\_patches | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list device groups'
List all device groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.CollectionID | string | 
action\_result\.data\.\*\.CollectionRules | string | 
action\_result\.data\.\*\.CollectionType | string | 
action\_result\.data\.\*\.CollectionVariablesCount | string | 
action\_result\.data\.\*\.Comment | string | 
action\_result\.data\.\*\.CurrentStatus | string | 
action\_result\.data\.\*\.HasProvisionedMember | string | 
action\_result\.data\.\*\.ISVData | string | 
action\_result\.data\.\*\.ISVDataSize | string | 
action\_result\.data\.\*\.ISVString | string | 
action\_result\.data\.\*\.IncludeExcludeCollectionsCount | string | 
action\_result\.data\.\*\.IsBuiltIn | string | 
action\_result\.data\.\*\.IsReferenceCollection | string | 
action\_result\.data\.\*\.LastChangeTime | string | 
action\_result\.data\.\*\.LastMemberChangeTime | string | 
action\_result\.data\.\*\.LastRefreshTime | string | 
action\_result\.data\.\*\.LimitToCollectionID | string | 
action\_result\.data\.\*\.LimitToCollectionName | string | 
action\_result\.data\.\*\.LocalMemberCount | string | 
action\_result\.data\.\*\.MemberClassName | string | 
action\_result\.data\.\*\.MemberCount | string | 
action\_result\.data\.\*\.MonitoringFlags | string | 
action\_result\.data\.\*\.Name | string |  `sccm device group name` 
action\_result\.data\.\*\.ObjectPath | string | 
action\_result\.data\.\*\.OwnedByThisSite | string | 
action\_result\.data\.\*\.PSComputerName | string |  `host name` 
action\_result\.data\.\*\.PSShowComputerName | string | 
action\_result\.data\.\*\.PowerConfigsCount | string | 
action\_result\.data\.\*\.RefreshSchedule | string | 
action\_result\.data\.\*\.RefreshType | string | 
action\_result\.data\.\*\.ReplicateToSubSites | string | 
action\_result\.data\.\*\.ServiceWindowsCount | string | 
action\_result\.data\.\*\.SmsProviderObjectPath | string | 
action\_result\.data\.\*\.UseCluster | string | 
action\_result\.summary\.total\_device\_groups | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 