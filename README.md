# Provisioning AWS SSO talking to Azure Active Directory
A collection of helper functions and a sample script to provision a SAML Provider and an associated role to AWS

(For provisioning a SAML Provider in AWS through cloudformation directly see colin Panisset's repo here: <https://github.com/cevoaustralia/cfn-identity-provider>)

 Helper functions for: 
- creating/finding/deleting a SAML provider via API calls
- creating/finding an IAM role via API calls
- creating/finding/deleting clou
- generating the role json to paste into the AWS application manifest in Active Directory

### Note: 
This only covers the AWS side of the SAML Provider provisioning. 

## Demo Scripts 

### provisioner.py
A demo script for provisioning a SAML Provider and A cloudfromation stack to define a trust role.

You can provide any cloudfromation template you like. 

#### A Note on parameters... 
If you parameter file contain a parameter called `SAMLProviderARN` and/or `RoleName` it will be overwritten with the correct values
for the data provided on the command line. The `SAMLProviderARN` value will be either the ARN of the new SAML provider created or,
if that one already exists, set to the ARN of the existing SAML provider (looked up by name). `RoleName` will be set to whatever is
passed in through the `-r/--role_name` command line parameter 

```
usage: provisioner.py [-h] -m --saml_metadata SAML_METADATA -t --cfn_template
                      TEMPLATE_PATH [-p --cfn_parameters PARAMS_FILE]
                      [-s --stack_name STACK_NAME]
                      [-i --idp_name PROVIDER_NAME] [-r --role_name ROLE_NAME]
                      [-d --role_description ROLE_DESCRIPTION]

Set up AWS account for SAML auth

optional arguments:
  -h, --help            show this help message and exit
  -m --saml_metadata SAML_METADATA
                        file containing AD cert metadata
  -t --cfn_template TEMPLATE_PATH
                        path to cloudformation template
  -p --cfn_parameters PARAMS_FILE
                        path to cloudformation parameters file
  -s --stack_name STACK_NAME
                        name of the cloudformation stack
  -i --idp_name PROVIDER_NAME
                        name to assign to the identity provider
  -r --role_name ROLE_NAME
                        name to assign to the role created
  -d --role_description ROLE_DESCRIPTION
                        description to assign to the role created
```

### deprovisioner.py
A script to tear down the stack and SAML provider created by `provisioner.py`

```
usage: deprovisioner.py [-h] -s --stack_name STACK_NAME -p
                        --saml_provider_name SAML_PROVIDER_NAME

Set up AWS account for SAML auth

optional arguments:
  -h, --help            show this help message and exit
  -s --stack_name STACK_NAME
                        name of the cloudformation stack
  -p --saml_provider_name SAML_PROVIDER_NAME
                        name to assign to the identity provider
```
