[comment]: # "    File: README.md"
[comment]: # "  Copyright (c) 2017-2024 Splunk Inc."
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

The use of the HTTP_PROXY and HTTPS_PROXY environment variables is
currently unsupported.

### Authentication

This app uses different default authorisation method, when FIPS is enabled:
| FIPS     | Default auth |
|----------|--------------|
| Enabled  | Basic HTTP   |
| Disabled | NTLM         |

In asset configuration more authentication types can be selected:
* certificate
* credssp
* ntlm
* basic
* kerberos (Currently a Kerberos ticket needs to be initialized outside of pywinrm using the kinit command)

### Certificate Authentication

To authenticate using SSL certificates, select `certificate` authentication in asset configuration method and pass following configuration parameters.

* cert_pem_path - A path to signed certificate file that is trusted by the Windows instance, in PEM format

* cert_key_pem_path - A filepath to key used to generate cert_pem file

* ca_trust_path - The certificate of the certificate authority that signed cert_file. It's needed only when you set up your own certificate authority.

It is recommended that these files be placed under the <PHANTOM_HOME>/etc/ssl/ directory. These files must be readable by the phantom-worker user.

### Kerberos Authentication

To authenticate using Kerberos, select `kerberos` authentication in asset configuration and provide hostname and username used for authorization.
You'll also need to setup your Phantom VM to support Kerberos:

-  Kerberos packages needs to be installed: `krb5-workstation krb5-libs krb5-auth-dialog`
-  `/etc/krb5.conf` needs to be properly configured for your realm and kdc
-  If there is no DNS configuration, `hosts` file will need to have mappings for server with mssccm under same domain as on Windows server 
-  `kinit` must be run for principal that will be used to connect to msccm
-   It should be noted that Kerberos tickets will expire, so it is recommended to use a script to
    run `kinit` periodically to refresh the ticket for the user, alternatively `keytab` file can be created on server and used on client for connectivity.
