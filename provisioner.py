"""
Creates a SAML provider and associated trust role with no attached policies in the current account.
Also creates a json blob to paste in the AWS application manifest in AD
"""
import json

from provisioner.iam_helpers import saml, roles
from provisioner.cfn_helpers.stacks import create_stack, update_stack
from provisioner.cfn_helpers.templates import validate_template
from provisioner.exceptions import (SAMLProviderExistsError,
                                    NoUpdateToPerformError,
                                    StackExistsError,
                                    RoleNotFoundError)
from provisioner.ad_helpers import approles

def main(args):
    "Let's make us some roles!"
    print("Adding SAML provider to Account...")
    saml_provider_arn = None
    stack_name = args.stack_name
    role_name = args.role_name
    template_path = args.template_path
    try:
        saml_provider_arn = saml.add_saml_provider(args.saml_metadata, args.provider_name)
    except SAMLProviderExistsError:
        print("SAML provider {} already exists. Looking up ARN...".format(args.provider_name))
        saml_provider_arn = saml.look_up_saml_provider(args.provider_name)
    print("Identity Provider: {}".format(saml_provider_arn))

    print("Adding Role to account...")
    try:
        parameters = [
            {
                "ParameterKey": "SAMLProviderARN",
                "ParameterValue": saml_provider_arn
            },
            {
                "ParameterKey": "RoleName",
                "ParameterValue": role_name
            }
        ]
        print("Validating template '{}'".format(template_path))
        validate_template(template_path)
        stack_id = create_stack(stack_name, template_path, parameters)
        print("Stack created. ID: {}".format(stack_id))
    except StackExistsError:
        print("Stack {} already exists. Updating stack instead.".format(stack_name))
        try:
            response = update_stack(stack_name, template_path, parameters)
            print("Stack updated successfully. Response: {}".format(response))
        except NoUpdateToPerformError:
            print("Stack does not require Updating.")

    print("Looking up role ARN...")
    try:
        role_data = roles.look_up_role(role_name)
        trust_role_arn = role_data['Role']['Arn']
        print("Role Found: {}".format(trust_role_arn))
    except RoleNotFoundError:
        print("Couldn't find role {}".format(role_name))
        raise

    print("Generating appRoles JSON blob...")
    approles_blob = approles.generate_ad_role(args.role_name,
                                              args.role_description,
                                              trust_role_arn,
                                              saml_provider_arn)
    print("appRoles json generated:")
    print(json.dumps(approles_blob, sort_keys=True, indent=4))


if __name__ == "__main__":
    import argparse
    __parser__ = argparse.ArgumentParser(description="Set up AWS account for SAML auth")
    __parser__.add_argument('-m --saml_metadata',
                            type=str,
                            required=True,
                            help='file containing AD cert metadata',
                            dest='saml_metadata')
    __parser__.add_argument('-c --cfn-template',
                            type=str,
                            required=True,
                            help='path to cloudformation templates specifying role and policy doc',
                            dest='template_path')
    __parser__.add_argument('-s --stack_name',
                            type=str,
                            help='name of the cloudformation stack',
                            dest='stack_name',
                            default='federated-trust-role-and-policy')
    __parser__.add_argument('-i --idp_name',
                            type=str,
                            help='name to assign to the identity provider',
                            dest="provider_name",
                            default="new_saml_provider")
    __parser__.add_argument('-r --role_name',
                            type=str,
                            help="name to assign to the role created",
                            dest="role_name",
                            default="new_saml_role")
    __parser__.add_argument('-d --role_description',
                            type=str,
                            help="description to assign to the role created",
                            dest="role_description",
                            default="A role created by")
    __args__ = __parser__.parse_args()
    main(__args__)
