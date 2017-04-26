"""
Creates a SAML provider and associated trust role with no attached policies in the current account.
Also creates a json blob to paste in the AWS application manifest in AD
"""
import json

from provisioner.iam_helpers import saml
from provisioner.iam_helpers import roles
from provisioner.ad_helpers import approles

def main(args):
    "Let's make us some roles!"
    print("Adding SAML provider to Account...")
    saml_provider_arn = saml.add_saml_provider(args.saml_metadata, args.provider_name)
    print("Identity Provider created: {}".format(saml_provider_arn))
    print("Adding Role to account...")
    trust_role_arn = roles.add_trust_role(args.role_template,
                                          saml_provider_arn,
                                          args.role_name,
                                          args.role_description)
    print("Trust role created: {}".format(trust_role_arn))
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
    __parser__.add_argument('-s --saml_metadata',
                            type=str,
                            help='file containing AD cert metadata',
                            dest='saml_metadata')
    __parser__.add_argument('-r --role_template',
                            type=str,
                            help='file containing the template for the role',
                            dest='role_template')
    __parser__.add_argument('-i --idp_name',
                            type=str,
                            help='name to assign to the identity provider',
                            dest="provider_name",
                            default="new_saml_provider")
    __parser__.add_argument('-n --role_name',
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
