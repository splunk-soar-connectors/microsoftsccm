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
