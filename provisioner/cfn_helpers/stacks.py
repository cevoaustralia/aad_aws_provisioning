"""
Collection of functions for dealing with cloudformation stacks.
"""
import logging
from beautifultable import BeautifulTable
import boto3
from botocore.exceptions import ClientError, WaiterError
from provisioner.exceptions import StackExistsError, NoUpdateToPerformError

__logger__ = logging.getLogger(__name__)
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
            __logger__.debug(response)
            __logger__.info("Waiting for stack creation to complete...")
            complete_waiter.wait(StackName=stack_name)
            return response['StackId']
    except FileNotFoundError:
        __logger__.error("Unable to locate template file '%s'", template_path)
        raise
    except WaiterError as waiter_error:
        __logger__.error("Something went wrong creating the stack! %s", waiter_error)
        print_stack_events(stack_name, 150)
        raise
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'AlreadyExistsException':
            __logger__.warning("Cloudformation Stack '%s' already exists...", stack_name)
            raise StackExistsError(stack_name)
        else:
            __logger__.error("There was an error validating the template: %s", str(client_error))
            raise

def update_stack(stack_name, template_path, parameters):
    """
    Update an existing cloudformation stack
    """
    try:
        update_waiter = __client__.get_waiter('stack_update_complete')
        with open(template_path, 'r') as template_body:
            response = __client__.update_stack(
                StackName=stack_name,
                TemplateBody=template_body.read(),
                Parameters=parameters,
                Capabilities=[
                    'CAPABILITY_NAMED_IAM'
                ]
            )
            __logger__.debug(response)
            __logger__.info("Waiting for stack '%s' to update...", stack_name)
            update_waiter.wait(StackName=stack_name)
            return response
    except FileNotFoundError:
        __logger__.error("Unable to locate template file '%s'", template_path)
        raise
    except WaiterError as waiter_error:
        __logger__.error("Something went wrong updating the stack! %s", waiter_error)
        print_stack_events(stack_name, 150)
        raise
    except ClientError as client_error:
        if client_error.response['Error']['Message'] == 'No updates are to be performed.':
            __logger__.warning("Stack '%s' is up to date with template '%s'",
                               stack_name,
                               template_path)
            raise NoUpdateToPerformError(stack_name)
        else:
            __logger__.error("Error Updating Stack %s: %s", stack_name, client_error)
            raise

def delete_stack(stack_name):
    """
    Delete a stack
    """
    try:
        delete_waiter = __client__.get_waiter('stack_delete_complete')
        response = __client__.delete_stack(StackName=stack_name)
        __logger__.info("Waiting for stack '%s' to be deleted...", stack_name)
        delete_waiter.wait(StackName=stack_name)
        return response
    except WaiterError as waiter_error:
        __logger__.error("Something went wrong deleting the stack! '%s'", waiter_error)
        print_stack_events(stack_name, 150)
        raise
    except ClientError as client_error:
        __logger__.error("Something went wrong deleting stack '%s': %s", stack_name, client_error)
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
        __logger__.error("Error describing stack '%s'", stack_name)
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
