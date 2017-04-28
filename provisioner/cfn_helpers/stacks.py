"""
Collection of functions for dealing with cloudformation stacks.
"""

import boto3

__client__ = boto3.client("cloudformation", region_name="ap-southeast-2")

def create_stack(stack_name, template, parameters):
    """
    Create a cloudformation stack in the current account
    """
    response = __client__.create_stack(
        StackName=stack_name,
        TemplateBody=template,
        Parameters=parameters,
        TimeoutInMinutes=5,
        Capabilities=[
            'CAPABILITY_NAMED_IAM'
        ],
        OnFailure='ROLLBACK'
    )
    print(response)

    return response['StackId']
