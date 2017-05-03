"""
Tear down a provisioned stack and remove the SAML provider for cleanup.
"""

from provisioner.cfn_helpers.stacks import delete_stack
from provisioner.iam_helpers.saml import look_up_saml_provider, delete_saml_provider

def main(args):
    """
    Tear it down!
    """
    print("Destroying all your good work!")

# firstly tear down the cloudformation stack
    print("Removing stack '{}'".format(args.stack_name))
    delete_stack(args.stack_name)

# then remove the SAML provider.
    print("Removing SAML provider '{}'".format(args.saml_provider_name))
    # need the ARN of the saml provider, so lets look it up

    saml_provider_arn = look_up_saml_provider(args.saml_provider_name)
    delete_saml_provider(saml_provider_arn)

if __name__ == "__main__":
    import argparse
    __parser__ = argparse.ArgumentParser(description="Set up AWS account for SAML auth")
    __parser__.add_argument('-s --stack_name',
                            type=str,
                            help='name of the cloudformation stack',
                            dest='stack_name',
                            required=True,
                            default='federated-trust-role-and-policy')
    __parser__.add_argument('-p --saml_provider_name',
                            type=str,
                            help='name to assign to the identity provider',
                            dest="saml_provider_name",
                            required=True,
                            default="new_saml_provider")
    __args__ = __parser__.parse_args()
    main(__args__)
