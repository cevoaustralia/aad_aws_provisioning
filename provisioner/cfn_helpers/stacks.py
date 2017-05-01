"""
Collection of functions for dealing with cloudformation stacks.
"""

import boto3
from botocore.exceptions import ClientError
from provisioner.exceptions import StackExistsError

__client__ = boto3.client("cloudformation", region_name="ap-southeast-2")

def create_stack(stack_name, template_path, parameters):
    """
    Create a cloudformation stack in the current account
    """
    try:
        with open(template_path, 'r') as template_body:
            response = __client__.create_stack(
                StackName=stack_name,
                TemplateBody=template_body.read(),
                Parameters=parameters,
                TimeoutInMinutes=5,
                Capabilities=[
                    'CAPABILITY_NAMED_IAM'
                ],
                OnFailure='ROLLBACK'
            )
            print(response)

            return response['StackId']
    except FileNotFoundError:
        print("Unable to locate template file {}".format(template_path))
        raise
    except ClientError as client_error:
        print("Fooooo")
        if client_error.response['Error']['Code'] == 'AlreadyExistsException':
            print("SAML provider already exists...")
            raise StackExistsError(stack_name)
        else:
            print("There was an error validating the template: " + str(client_error))
            raise
