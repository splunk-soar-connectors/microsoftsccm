**Unreleased**

* [SOARHELP-2713] Authentication method selection is available in asset configuration. 
    * User can choose between: default, ssl, basic, credssp, ntlm.  
    * Default method means that while FIPS is enabled Basic HTTP will be used, otherwise NTLM will be applied
