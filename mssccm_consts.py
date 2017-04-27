# --
# File: mssccm_consts.py
#
# Copyright (c) Phantom Cyber Corporation, 2016
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --

MSSCCM_ERR_SERVICE_INSTALLATION = "Service installation failed. Please make sure phantom can connect to the host and has the neccessary credentials."
MSSCCM_ERR_SERVICE_UNINSTALLATION = "Service uninstallation failed"
MSSCCM_ERR_NEITHER_PID_NOR_PNAME = "Please specify either pid or process name."
MSSCCM_MSG_UNINSTALLING_SERVICE = "Uninstalling service"
MSSCCM_ERR_SOCKET_CONNECT = "Unable to communicate with Phantom service."
MSSCCM_ERR_SOCKET_CONNECT += "\nThe service after installation tries to connect to the Phantom appliance over TCP."
MSSCCM_ERR_SOCKET_CONNECT += "\nPlease ensure this communication is allowed between the  two endpoints"
MSSCCM_ERR_NO_DATA = "Did not recieve any data from the Phantom service."
MSSCCM_ERR_NO_DATA += "\nThis usually happens if the service was unable to authenticate the Phantom device"

MSSCCM_ERR_SOCKET_DATA = "Unable to read data from Phantom service"
MSSCCM_ERR_SOCKET_NOT_CONNECTED = "Unable to communicate with Phantom service. Socket not created"
MSSCCM_MSG_PROG_SENDING_COMMAND_TO = "Sending command to {machine}"
MSSCCM_ERR_INVALID_MACHINE_NAME_IP = "Invalid machine name/IP"
MSSCCM_SUCC_FILE_ADD_TO_VAULT = "File added to vault with ID: {vault_id}"
MSSCCM_ERR_FAILED_TO_GET_FREE_PORT = "Failed to get free port to bind on"
MSSCCM_ERR_FAILED_TO_GET_IP_FOR_INTERFACE = "Failed to get ip address for interface '{interface}'"
MSSCCM_ERR_IP_NOT_FOUND = "Unable to find ip for interface '{interface}'"
MSSCCM_ERR_PARSE_PORT_RANGE = "Unable to parse the port range string"

MSSCCM_LISTENING_FOR_CONNECTIONS = "Listening for connection from Phantom Agent on {ip}:{port}"
MSSCCM_ACCEPTED_CONNECTION_FROM = "Accepted connection from {ip}:{port}"
MSSCCM_COMMUNICATING_CHANNEL = "Communicating on channel"
MSSCCM_SSL_CONNECTION_ESTABLISHED = "SSL connection established"

MSSCCM_PROCESS_IMAGE = "pe file"
MSSCCM_PROCESS_DUMP = "process dump"

MSSCCM_JSON_UNINSTALL_SERVICE = "uninstall_service"
MSSCCM_JSON_PID = "pid"
MSSCCM_JSON_NAME = "name"
MSSCCM_JSON_COMMAND = "program"
MSSCCM_JSON_ARGS = "args"
MSSCCM_JSON_MESSAGE = "message"
MSSCCM_JSON_WAITTIME = "wait_time"
MSSCCM_JSON_LOCAL_ADDR = "local_addr"
MSSCCM_JSON_LOCAL_PORT = "local_port"
MSSCCM_JSON_REMOTE_ADDR = "remote_addr"
MSSCCM_JSON_REMOTE_PORT = "local_port"

MSSCCM_JSON_REMOTE_IP = "remote_ip"
MSSCCM_JSON_REMOTE_PORT = "remote_port"
MSSCCM_JSON_DIR = "dir"
MSSCCM_JSON_LOCAL_PROTOCOL = "protocol"
MSSCCM_JSON_FW_RULE_NAME = "rule_name"
MSSCCM_JSON_BASE64_ZIP = "file_base64_zip_content"
MSSCCM_JSON_FILE_NAME = "file_name"
MSSCCM_JSON_FILE_SIZE = "file_comp_size"
MSSCCM_JSON_INTERFACE = "interface"
MSSCCM_JSON_PORT_RANGE = "port_range"
MSSCCM_JSON_USER_IDENTITY = "user"
UPDATE_PERFORM_COMMAND = "\n\n\nGet-WUInstall -KBArticleID $KBList -AcceptAll"
MSSCCM_JSON_SUBJECT = "subject"
MSSCCM_JSON_FROM = "from"
MSSCCM_JSON_DESTINATION_MAILBOX = "destination_mailbox"
MSSCCM_JSON_DESTINATION_FOLDER = "destination_folder"
MSSCCM_JSON_TOTAL_EMAIL_MATCHES = "total_emails_matched"
MSSCCM_JSON_TOTAL_MBOXES = "total_mailboxes_matched"

WIN7_INSTALLER = "/opt/phantom/bin/instsvcwin7"
WINXP_INSTALLER = "/opt/phantom/bin/instsvcxp"
SVC_INST_PARAMS = ["--svcinst", "--svcfileprefix=/opt/phantom/bin/win/phsvc", "--svcbinname=phantom_agent.exe"]
SVC_PARAMS = "--svcparams=-service -a {ip} -p {port}"

SVC_UNINST_PARAMS = "--svcuninst --svcbinname=phantom_agent.exe"
SERVICE_PORT = 27015
RECV_BUF_SIZE = 4096
DEFAULT_MIN_WAIT_TIME = 10
MSSCCM_FW_RULE_PREFIX = "PH_FW_RULE_"

DEFAULT_MIN_PORT = 27100
DEFAULT_MAX_PORT = 27200
CERT_PATH = "/etc/ssl/certs/httpd_cert.crt"
CERT_KEY_PATH = "/etc/ssl/private/httpd_cert.key"
DEFAULT_INTERFACE_NAME = "eth1"
LISTEN_TIMEOUT = 240  # seconds

WINAGENT_CMD_RUN_PS_SCRIPT = "run_ps_script"
WINAGENT_CMD_PS_PARAMS = "ps_params"  # params to the powershell exe
WINAGENT_CMD_PS_SCRIPT_CODE = "script_code"  # the script code
WINAGENT_CMD_PS_SCRIPT_NAME = "script_name"  # script name to use
WINAGENT_CMD_SCRIPT_PARAMS = "script_params"  # params to pass to the script
get_update_definition = """
Function Get-WUList
{
[OutputType('PSWindowsUpdate.WUList')]
[CmdletBinding(
SupportsShouldProcess=$True,
ConfirmImpact="High"
)]
Param
(
[ValidateSet("Driver", "Software")]
[String]$UpdateType="",
[String[]]$UpdateID,
[Int]$RevisionNumber,
[String[]]$CategoryIDs,
[Switch]$IsInstalled,
[Switch]$IsHidden,
[Switch]$IsNotHidden,
[String]$Criteria,
[Switch]$ShowSearchCriteria,
[String[]]$Category="",
[String[]]$KBArticleID,
[String]$Title,
[String[]]$NotCategory="",
[String[]]$NotKBArticleID,
[String]$NotTitle,
[Alias("Silent")]
[Switch]$IgnoreUserInput,
[Switch]$IgnoreRebootRequired,
[Switch]$AutoSelectOnly,
[String]$ServiceID,
[Switch]$WindowsUpdate,
[Switch]$MicrosoftUpdate,
[Switch]$Debuger,
[parameter(ValueFromPipeline=$true,
ValueFromPipelineByPropertyName=$true)]
[String[]]$ComputerName
)
Begin
{
If($PSBoundParameters['Debuger'])
{
$DebugPreference = "Continue"
}
$User = [Security.Principal.WindowsIdentity]::GetCurrent()
$Role = (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}
Process
{
If($ComputerName -eq $null)
{
[String[]]$ComputerName = $env:COMPUTERNAME
}
$UpdateCollection = @()
Foreach($Computer in $ComputerName)
{
If(Test-Connection -ComputerName $Computer -Quiet)
{
If($Computer -eq $env:COMPUTERNAME)
{
$objServiceManager = New-Object -ComObject "Microsoft.Update.ServiceManager"
$objSession = New-Object -ComObject "Microsoft.Update.Session"
}
Else
{
$objSession =  [activator]::CreateInstance([type]::GetTypeFromProgID("Microsoft.Update.Session",$Computer))
}
$objSearcher = $objSession.CreateUpdateSearcher()
If($WindowsUpdate)
{
$objSearcher.ServerSelection = 2
$serviceName = "Windows Update"
}
ElseIf($MicrosoftUpdate)
{
$serviceName = $null
Foreach ($objService in $objServiceManager.Services)
{
If($objService.Name -eq "Microsoft Update")
{
$objSearcher.ServerSelection = 3
$objSearcher.ServiceID = $objService.ServiceID
$serviceName = $objService.Name
Break
}
}
If(-not $serviceName)
{
Return
}
}
ElseIf($Computer -eq $env:COMPUTERNAME)
{
Foreach ($objService in $objServiceManager.Services)
{
If($ServiceID)
{
If($objService.ServiceID -eq $ServiceID)
{
$objSearcher.ServiceID = $ServiceID
$objSearcher.ServerSelection = 3
$serviceName = $objService.Name
Break
}
}
Else
{
If($objService.IsDefaultAUService -eq $True)
{
$serviceName = $objService.Name
Break
}
}
}
}
ElseIf($ServiceID)
{
$objSearcher.ServiceID = $ServiceID
$objSearcher.ServerSelection = 3
$serviceName = $ServiceID
}
Else
{
$serviceName = "default (for $Computer) Windows Update"
}
Try
{
$search = ""
If($Criteria)
{
$search = $Criteria
}
Else
{
If($IsInstalled)
{
$search = "IsInstalled = 1"
}
Else
{
$search = "IsInstalled = 0"
}
If($UpdateType -ne "")
{
$search += " and Type = '$UpdateType'"
}
If($UpdateID)
{
$tmp = $search
$search = ""
$LoopCount = 0
Foreach($ID in $UpdateID)
{
If($LoopCount -gt 0)
{
$search += " or "
}
If($RevisionNumber)
{
$search += "($tmp and UpdateID = '$ID' and RevisionNumber = $RevisionNumber)"
}
Else
{
$search += "($tmp and UpdateID = '$ID')"
}
$LoopCount++
}
}
If($CategoryIDs)
{
$tmp = $search
$search = ""
$LoopCount =0
Foreach($ID in $CategoryIDs)
{
If($LoopCount -gt 0)
{
$search += " or "
}
$search += "($tmp and CategoryIDs contains '$ID')"
$LoopCount++
}
}
If($IsNotHidden)
{
$search += " and IsHidden = 0"
}
ElseIf($IsHidden)
{
$search += " and IsHidden = 1"
}
If($IgnoreRebootRequired)
{
$search += " and RebootRequired = 0"
}
}
If($ShowSearchCriteria)
{
}
$objResults = $objSearcher.Search($search)
}
Catch
{
Return
}
$NumberOfUpdate = 1
$PreFoundUpdatesToDownload = $objResults.Updates.count
If($PreFoundUpdatesToDownload -eq 0)
{
Continue
}
Foreach($Update in $objResults.Updates)
{
$UpdateAccess = $true
If($Category -ne "")
{
$UpdateCategories = $Update.Categories | Select-Object Name
Foreach($Cat in $Category)
{
If(!($UpdateCategories -match $Cat))
{
$UpdateAccess = $false
}
Else
{
$UpdateAccess = $true
Break
}
}
}
If($NotCategory -ne "" -and $UpdateAccess -eq $true)
{
$UpdateCategories = $Update.Categories | Select-Object Name
Foreach($Cat in $NotCategory)
{
If($UpdateCategories -match $Cat)
{
$UpdateAccess = $false
Break
}
}
}
If($KBArticleID -ne $null -and $UpdateAccess -eq $true)
{
If(!($KBArticleID -match $Update.KBArticleIDs -and "" -ne $Update.KBArticleIDs))
{
$UpdateAccess = $false
}
}
If($NotKBArticleID -ne $null -and $UpdateAccess -eq $true)
{
If($NotKBArticleID -match $Update.KBArticleIDs -and "" -ne $Update.KBArticleIDs)
{
$UpdateAccess = $false
}
}
If($Title -and $UpdateAccess -eq $true)
{
If($Update.Title -notmatch $Title)
{
$UpdateAccess = $false
}
}
If($NotTitle -and $UpdateAccess -eq $true)
{
If($Update.Title -match $NotTitle)
{
$UpdateAccess = $false
}
}
If($IgnoreUserInput -and $UpdateAccess -eq $true)
{
If($Update.InstallationBehavior.CanRequestUserInput -eq $true)
{
$UpdateAccess = $false
}
}
If($IgnoreRebootRequired -and $UpdateAccess -eq $true)
{
If($Update.InstallationBehavior.RebootBehavior -ne 0)
{
$UpdateAccess = $false
}
}
If($AutoSelectOnly -and $UpdateAccess -eq $true)
{
If($Update.AutoSelectOnWebsites -ne $true)
{
$UpdateAccess = $false
}
}
If($UpdateAccess -eq $true)
{
Switch($Update.MaxDownloadSize)
{
{[System.Math]::Round($_/1KB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1KB,0))+" KB"; break }
{[System.Math]::Round($_/1MB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1MB,0))+" MB"; break }
{[System.Math]::Round($_/1GB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1GB,0))+" GB"; break }
{[System.Math]::Round($_/1TB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1TB,0))+" TB"; break }
default { $size = $_+"B" }
}
If($Update.KBArticleIDs -ne "")
{
$KB = "KB"+$Update.KBArticleIDs
}
Else
{
$KB = ""
}
$Status = ""
        If($Update.IsDownloaded)    {$Status += "D"} else {$status += "-"}
        If($Update.IsInstalled)     {$Status += "I"} else {$status += "-"}
        If($Update.IsMandatory)     {$Status += "M"} else {$status += "-"}
        If($Update.IsHidden)        {$Status += "H"} else {$status += "-"}
        If($Update.IsUninstallable) {$Status += "U"} else {$status += "-"}
        If($Update.IsBeta)          {$Status += "B"} else {$status += "-"}
Add-Member -InputObject $Update -MemberType NoteProperty -Name ComputerName -Value $Computer
Add-Member -InputObject $Update -MemberType NoteProperty -Name KB -Value $KB
Add-Member -InputObject $Update -MemberType NoteProperty -Name Size -Value $size
Add-Member -InputObject $Update -MemberType NoteProperty -Name Status -Value $Status
$Update.PSTypeNames.Clear()
$Update.PSTypeNames.Add('PSWindowsUpdate.WUList')
$UpdateCollection += $Update
}
$NumberOfUpdate++
}
$FoundUpdatesToDownload = $UpdateCollection.count
}
}
Return $UpdateCollection
}
End{}
}"""

perform_update_definition = """
Function Get-WUInstall
{
[OutputType('PSWindowsUpdate.WUInstall')]
[CmdletBinding(
SupportsShouldProcess=$True,
ConfirmImpact="High"
)]
Param
(
[parameter(ValueFromPipelineByPropertyName=$true)]
[ValidateSet("Driver", "Software")]
[String]$UpdateType="",
[parameter(ValueFromPipelineByPropertyName=$true)]
[String[]]$UpdateID,
[parameter(ValueFromPipelineByPropertyName=$true)]
[Int]$RevisionNumber,
[parameter(ValueFromPipelineByPropertyName=$true)]
[String[]]$CategoryIDs,
[parameter(ValueFromPipelineByPropertyName=$true)]
[Switch]$IsInstalled,
[parameter(ValueFromPipelineByPropertyName=$true)]
[Switch]$IsHidden,
[parameter(ValueFromPipelineByPropertyName=$true)]
[Switch]$WithHidden,
[String]$Criteria,
[Switch]$ShowSearchCriteria,
[parameter(ValueFromPipelineByPropertyName=$true)]
[String[]]$Category="",
[parameter(ValueFromPipelineByPropertyName=$true)]
[String[]]$KBArticleID,
[parameter(ValueFromPipelineByPropertyName=$true)]
[String]$Title,
[parameter(ValueFromPipelineByPropertyName=$true)]
[String[]]$NotCategory="",
[parameter(ValueFromPipelineByPropertyName=$true)]
[String[]]$NotKBArticleID,
[parameter(ValueFromPipelineByPropertyName=$true)]
[String]$NotTitle,
[parameter(ValueFromPipelineByPropertyName=$true)]
[Alias("Silent")]
[Switch]$IgnoreUserInput,
[parameter(ValueFromPipelineByPropertyName=$true)]
[Switch]$IgnoreRebootRequired,
[String]$ServiceID,
[Switch]$WindowsUpdate,
[Switch]$MicrosoftUpdate,
[Switch]$ListOnly,
[Switch]$DownloadOnly,
[Alias("All")]
[Switch]$AcceptAll,
[Switch]$AutoReboot,
[Switch]$IgnoreReboot,
[Switch]$AutoSelectOnly,
[Switch]$Debuger
)
Begin
{
If($PSBoundParameters['Debuger'])
{
$DebugPreference = "Continue"
}
$User = [Security.Principal.WindowsIdentity]::GetCurrent()
$Role = (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}
Process
{
If($IsInstalled)
{
$ListOnly = $true
}
$objSystemInfo = New-Object -ComObject "Microsoft.Update.SystemInfo"
If($objSystemInfo.RebootRequired)
{
If($AutoReboot)
{
Restart-Computer -Force
}
If(!$ListOnly)
{
Return
}
}
If($ListOnly)
{
$NumberOfStage = 2
}
ElseIf($DownloadOnly)
{
$NumberOfStage = 3
}
Else
{
$NumberOfStage = 4
}
$objServiceManager = New-Object -ComObject "Microsoft.Update.ServiceManager"
$objSession = New-Object -ComObject "Microsoft.Update.Session"
$objSearcher = $objSession.CreateUpdateSearcher()
If($WindowsUpdate)
{
$objSearcher.ServerSelection = 2
$serviceName = "Windows Update"
}
ElseIf($MicrosoftUpdate)
{
$serviceName = $null
Foreach ($objService in $objServiceManager.Services)
{
If($objService.Name -eq "Microsoft Update")
{
$objSearcher.ServerSelection = 3
$objSearcher.ServiceID = $objService.ServiceID
$serviceName = $objService.Name
Break
}
}
If(-not $serviceName)
{
Return
}
}
Else
{
Foreach ($objService in $objServiceManager.Services)
{
If($ServiceID)
{
If($objService.ServiceID -eq $ServiceID)
{
$objSearcher.ServiceID = $ServiceID
$objSearcher.ServerSelection = 3
$serviceName = $objService.Name
Break
}
}
Else
{
If($objService.IsDefaultAUService -eq $True)
{
$serviceName = $objService.Name
Break
}
}
}
}
Try
{
$search = ""
If($Criteria)
{
$search = $Criteria
}
Else
{
If($IsInstalled)
{
$search = "IsInstalled = 1"
}
Else
{
$search = "IsInstalled = 0"
}
If($UpdateType -ne "")
{
$search += " and Type = '$UpdateType'"
}
If($UpdateID)
{
$tmp = $search
$search = ""
$LoopCount = 0
Foreach($ID in $UpdateID)
{
If($LoopCount -gt 0)
{
$search += " or "
}
If($RevisionNumber)
{
$search += "($tmp and UpdateID = '$ID' and RevisionNumber = $RevisionNumber)"
}
Else
{
$search += "($tmp and UpdateID = '$ID')"
}
$LoopCount++
}
}
If($CategoryIDs)
{
$tmp = $search
$search = ""
$LoopCount =0
Foreach($ID in $CategoryIDs)
{
If($LoopCount -gt 0)
{
$search += " or "
}
$search += "($tmp and CategoryIDs contains '$ID')"
$LoopCount++
}
}
If($IsHidden)
{
$search += " and IsHidden = 1"
}
Else
{
$search += " and IsHidden = 0"
}
If($IgnoreRebootRequired)
{
$search += " and RebootRequired = 0"
}
}
$objResults = $objSearcher.Search($search)
}
Catch
{
Return
}
$objCollectionUpdate = New-Object -ComObject "Microsoft.Update.UpdateColl"
$NumberOfUpdate = 1
$UpdateCollection = @()
$UpdatesExtraDataCollection = @{}
$PreFoundUpdatesToDownload = $objResults.Updates.count
Foreach($Update in $objResults.Updates)
{
$UpdateAccess = $true
If($Category -ne "")
{
$UpdateCategories = $Update.Categories | Select-Object Name
Foreach($Cat in $Category)
{
If(!($UpdateCategories -match $Cat))
{
$UpdateAccess = $false
}
Else
{
$UpdateAccess = $true
Break
}
}
}
If($NotCategory -ne "" -and $UpdateAccess -eq $true)
{
$UpdateCategories = $Update.Categories | Select-Object Name
Foreach($Cat in $NotCategory)
{
If($UpdateCategories -match $Cat)
{
$UpdateAccess = $false
Break
}
}
}
If($KBArticleID -ne $null -and $UpdateAccess -eq $true)
{
If(!($KBArticleID -match $Update.KBArticleIDs -and "" -ne $Update.KBArticleIDs))
{
$UpdateAccess = $false
}
}
If($NotKBArticleID -ne $null -and $UpdateAccess -eq $true)
{
If($NotKBArticleID -match $Update.KBArticleIDs -and "" -ne $Update.KBArticleIDs)
{
$UpdateAccess = $false
}
}
If($Title -and $UpdateAccess -eq $true)
{
If($Update.Title -notmatch $Title)
{
$UpdateAccess = $false
}
}
If($NotTitle -and $UpdateAccess -eq $true)
{
If($Update.Title -match $NotTitle)
{
$UpdateAccess = $false
}
}
If($IgnoreUserInput -and $UpdateAccess -eq $true)
{
If($Update.InstallationBehavior.CanRequestUserInput -eq $true)
{
$UpdateAccess = $false
}
}
If($IgnoreRebootRequired -and $UpdateAccess -eq $true)
{
If($Update.InstallationBehavior.RebootBehavior -ne 0)
{
$UpdateAccess = $false
}
}
If($UpdateAccess -eq $true)
{
Switch($Update.MaxDownloadSize)
{
{[System.Math]::Round($_/1KB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1KB,0))+" KB"; break }
{[System.Math]::Round($_/1MB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1MB,0))+" MB"; break }
{[System.Math]::Round($_/1GB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1GB,0))+" GB"; break }
{[System.Math]::Round($_/1TB,0) -lt 1024} { $size = [String]([System.Math]::Round($_/1TB,0))+" TB"; break }
default { $size = $_+"B" }
}
If($Update.KBArticleIDs -ne "")
{
$KB = "KB"+$Update.KBArticleIDs
}
Else
{
$KB = ""
}
If($ListOnly)
{
$Status = ""
If($Update.IsDownloaded)    {$Status += "D"} else {$status += "-"}
If($Update.IsInstalled)     {$Status += "I"} else {$status += "-"}
If($Update.IsMandatory)     {$Status += "M"} else {$status += "-"}
If($Update.IsHidden)        {$Status += "H"} else {$status += "-"}
If($Update.IsUninstallable) {$Status += "U"} else {$status += "-"}
If($Update.IsBeta)          {$Status += "B"} else {$status += "-"}
Add-Member -InputObject $Update -MemberType NoteProperty -Name ComputerName -Value $env:COMPUTERNAME
Add-Member -InputObject $Update -MemberType NoteProperty -Name KB -Value $KB
Add-Member -InputObject $Update -MemberType NoteProperty -Name Size -Value $size
Add-Member -InputObject $Update -MemberType NoteProperty -Name Status -Value $Status
Add-Member -InputObject $Update -MemberType NoteProperty -Name X -Value 1
$Update.PSTypeNames.Clear()
$Update.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
$UpdateCollection += $Update
}
Else
{
$objCollectionUpdate.Add($Update) | Out-Null
$UpdatesExtraDataCollection.Add($Update.Identity.UpdateID,@{KB = $KB; Size = $size})
}
}
$NumberOfUpdate++
}
If($ListOnly)
{
$FoundUpdatesToDownload = $UpdateCollection.count
}
Else
{
$FoundUpdatesToDownload = $objCollectionUpdate.count
}
If($FoundUpdatesToDownload -eq 0)
{
Return
}
If($ListOnly)
{
Return $UpdateCollection
}
If(!$ListOnly)
{
$NumberOfUpdate = 1
$logCollection = @()
$objCollectionChoose = New-Object -ComObject "Microsoft.Update.UpdateColl"
Foreach($Update in $objCollectionUpdate)
{
$size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
If($AcceptAll)
{
$Status = "Accepted"
If($Update.EulaAccepted -eq 0)
{
$Update.AcceptEula()
}
$objCollectionChoose.Add($Update) | Out-Null
}
ElseIf($AutoSelectOnly)
{
If($Update.AutoSelectOnWebsites)
{
$Status = "Accepted"
If($Update.EulaAccepted -eq 0)
{
$Update.AcceptEula()
}

$objCollectionChoose.Add($Update) | Out-Null
}
Else
{
$Status = "Rejected"
}
}
Else
{
If($pscmdlet.ShouldProcess($Env:COMPUTERNAME,"$($Update.Title)[$size]?"))
{
$Status = "Accepted"
If($Update.EulaAccepted -eq 0)
{
$Update.AcceptEula()
}
$objCollectionChoose.Add($Update) | Out-Null
}
Else
{
$Status = "Rejected"
}
}
$log = New-Object PSObject -Property @{
Title = $Update.Title
KB = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].KB
Size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
Status = $Status
X = 2
}
$log.PSTypeNames.Clear()
$log.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
$logCollection += $log
$NumberOfUpdate++
}
$logCollection

$AcceptUpdatesToDownload = $objCollectionChoose.count
If($AcceptUpdatesToDownload -eq 0)
{
Return
}
$NumberOfUpdate = 1
$objCollectionDownload = New-Object -ComObject "Microsoft.Update.UpdateColl"
Foreach($Update in $objCollectionChoose)
{
$objCollectionTmp = New-Object -ComObject "Microsoft.Update.UpdateColl"
$objCollectionTmp.Add($Update) | Out-Null
$Downloader = $objSession.CreateUpdateDownloader()
$Downloader.Updates = $objCollectionTmp
Try
{
$DownloadResult = $Downloader.Download()
}
Catch
{
Return
}
Switch -exact ($DownloadResult.ResultCode)
{
0   { $Status = "NotStarted" }
1   { $Status = "InProgress" }
2   { $Status = "Downloaded" }
3   { $Status = "DownloadedWithErrors" }
4   { $Status = "Failed" }
5   { $Status = "Aborted" }
}
$log = New-Object PSObject -Property @{
Title = $Update.Title
KB = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].KB
Size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
Status = $Status
X = 3
}
$log.PSTypeNames.Clear()
$log.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
$log
If($DownloadResult.ResultCode -eq 2)
{
$objCollectionDownload.Add($Update) | Out-Null
}
$NumberOfUpdate++
}
$ReadyUpdatesToInstall = $objCollectionDownload.count
If($ReadyUpdatesToInstall -eq 0)
{
Return
}
If(!$DownloadOnly)
{
$NeedsReboot = $false
$NumberOfUpdate = 1
Foreach($Update in $objCollectionDownload)
{
$objCollectionTmp = New-Object -ComObject "Microsoft.Update.UpdateColl"
$objCollectionTmp.Add($Update) | Out-Null
$objInstaller = $objSession.CreateUpdateInstaller()
$objInstaller.Updates = $objCollectionTmp
Try
{
$InstallResult = $objInstaller.Install()
}
Catch
{
Return
}
If(!$NeedsReboot)
{
$NeedsReboot = $installResult.RebootRequired
}
Switch -exact ($InstallResult.ResultCode)
{
0   { $Status = "NotStarted"}
1   { $Status = "InProgress"}
2   { $Status = "Installed"}
3   { $Status = "InstalledWithErrors"}
4   { $Status = "Failed"}
5   { $Status = "Aborted"}
}
$log = New-Object PSObject -Property @{
Title = $Update.Title
KB = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].KB
Size = $UpdatesExtraDataCollection[$Update.Identity.UpdateID].Size
Status = $Status
X = 4
}
$log.PSTypeNames.Clear()
$log.PSTypeNames.Add('PSWindowsUpdate.WUInstall')
$log
$NumberOfUpdate++
}
}
}
}
End{}
}
"""
