# Provisioning AWS SSO talking to Azure Active Directory
```
usage: provisioner.py [-h] [-s --saml_metadata SAML_METADATA]
                      [-r --role_template ROLE_TEMPLATE]
                      [-i --idp_name PROVIDER_NAME] [-n --role_name ROLE_NAME]
                      [-d --role_description ROLE_DESCRIPTION]

Set up AWS account for SAML auth

optional arguments:
  -h, --help            show this help message and exit
  -s --saml_metadata SAML_METADATA
                        file containing AD cert metadata
  -r --role_template ROLE_TEMPLATE
                        file containing the template for the role
  -i --idp_name PROVIDER_NAME
                        name to assign to the identity provider
  -n --role_name ROLE_NAME
                        name to assign to the role created
  -d --role_description ROLE_DESCRIPTION
                        description to assign to the role created
```