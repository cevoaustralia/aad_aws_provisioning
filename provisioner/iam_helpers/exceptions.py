"""
Custom errors and exceptions for IAM helper functions
"""
class Error(Exception):
    """
    Base class for module Error handling
    """
    pass

class SAMLProviderExistsError(Error):
    """
    Exception raised when the SAML Provider already exists in the AWS Account
    """
    def __init__(self, provider):
        message = "SAML Provider {} already exists in this account.".format(provider)
        super().__init__(message)
        self.provider = provider
        self.message = message
