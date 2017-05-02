"""
Collection of functions for dealing with cloudformation stacks.
"""

from beautifultable import BeautifulTable
import boto3
from botocore.exceptions import ClientError, WaiterError
from provisioner.exceptions import StackExistsError

__client__ = boto3.client("cloudformation", region_name="ap-southeast-2")

def create_stack(stack_name, template_path, parameters):
    """
    Create a cloudformation stack in the current account
    """
    try:
        complete_waiter = __client__.get_waiter('stack_create_complete')
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
            print("Waiting for stack creation to complete...")
            complete_waiter.wait(StackName=stack_name)
            return response['StackId']
    except FileNotFoundError:
        print("Unable to locate template file {}".format(template_path))
        raise
    except WaiterError as waiter_error:
        print("Something went wrong creating the stack! {}".format(waiter_error))
        print_stack_events(stack_name, 150)
        raise
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'AlreadyExistsException':
            print("SAML provider already exists...")
            raise StackExistsError(stack_name)
        else:
            print("There was an error validating the template: " + str(client_error))
            raise

def get_stack_events(stack_name):
    """
    Return a simplified dict of stack events
    """

    try:
        response = __client__.describe_stack_events(StackName=stack_name)
        events = []
        for event in response['StackEvents']:
            timestamp = None
            resource = None
            status = None
            reason = None
            try:
                timestamp = event['Timestamp'].astimezone()
                resource = event['LogicalResourceId']
                status = event['ResourceStatus']
                reason = event['ResourceStatusReason']
            except KeyError:
                pass
            events.append([timestamp, resource, status, reason])
        return events
    except ClientError:
        print("Error describing stack {}".format(stack_name))
        raise

def print_stack_events(stack_name, table_width=80):
    """
    Print out stack events in a pretty table
    """
    stack_events = get_stack_events(stack_name)
    table = BeautifulTable(max_width=table_width)
    table.column_headers = ["Timestamp", "Resource", "Status", "Message"]
    for event in stack_events:
        table.append_row(event)
    table.sort('Timestamp')
    print("Stack Events:")
    print(table)
