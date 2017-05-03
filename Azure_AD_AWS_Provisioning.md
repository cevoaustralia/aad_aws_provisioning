Using Azure Active Directory (AD) to provide federated identity management to AWS
=================================================================================

## Cavaets
The process might be slightly different for using Office365 integration. This page: <https://jvzoggel.com/2015/10/16/cloud-integration-using-federation-between-microsoft-office-365-azure-active-directory-aad-and-amazon-web-service-aws/> seems to show thew same thing for Office365

## Prerequesites 
* AWS account
* Microsoft Azure Account (Free one month trial available. Note: you will need an Azure AD Premium account to do anything with groups)

## Connecting Azure AD and AWS for a single user
Follow the tutorial at:

<https://docs.microsoft.com/en-us/azure/active-directory/active-directory-saas-amazon-web-service-tutorial>

### Notes
* The tutorial above is for the AAD Classic interface. It was much easier to get this working with the old interface

* If you want to get this working in the new interface:  
    * Adding the Application to AD:
        * Click on `Enterprise Applications` under `Manage`
        * Click on `+ New Application` at the top of the screen
        * Search for `amazon web services` in the gallery
        * Click on the AWS app in the search results and click `Add` on the apps blade
        * wait for success message.
    * To find the app again: 
        * click on `Enterprise Apps` either in the breadcrumbs or the `Manage` menu of the AD hoempage     
    * Go to Single sign-on 
    * Set the following things:
        * Mode: SAML-based Sign-on
        * Show advanced URL Settings: ___LEAVE BLANK___
        * User Identifier: user.userprincipalname
    * download the Federation Cert from under the `SAML Signing Certificate` section

    * follow the original document to configure that AWS side of things. 

    * Set up the user attributes:
        * __WARNING: the new interface likes to convert attribute names to lowercase, which can break your saml call! Consider setting these in the old interface...__
        * Attributes:
            * for the role attribute:
                * Name: Role
                * Value: `<AWS role arn>,<AWS role Truseted Entity>`
                * Namespace: https://aws.amazon.com/SAML/Attributes
            * for the RoleSessionName attribute:
                * Name: RoleSessionName
                * Value: user.userprincipalname
                * NameSpace: https://aws.amazon.com/SAML/Attributes

    * tick `Make new certificate active`
    * Click `Save` at the top of the screen and `OK` on the popup. 

    * Click `Users and Groups` under `Manage`
    * Click `+Add user`  
    * Select a user from the Users list
    * Click `Assign`

* In theory everything should be set up now... 

* Log in to <https://account.activedirectory.windowsazure.com/applications/default.aspx> as the user you assigned access to to see if you app is working

* For command line access to Azure, I've found <https://github.com/dtjohnson/aws-azure-login> to work reasonably well. 

## Configuring AAD and AWS for multiple roles

Multiple roles can be assigned to users or groups by editing the manifest of the AWS application. 

* Edit the application manifest to add the custom roles

e.g.

```json
...
    "appRoles": [
        {
            "allowedMemberTypes": [
                "User"
            ],
            "displayName": "EC2-ReadOnly",
            "id": "3f73fb87-a2fe-48f6-ae7a-0842422017c0",
            "isEnabled": true,
            "description": "EC2 ReadOnly Access",
            "value": "arn:aws:iam::<AWS ACCT NUMBER>:role/EC2-ReadOnly,arn:aws:iam::<AWS ACCT NUMBER>:saml-provider/WAAD"
        },
        {
            "allowedMemberTypes": [
                "User"
            ],
            "displayName": "EC2-Admin",
            "id": "e7fb2c27-b333-491a-8c0c-5ab2eebbe034",
            "isEnabled": true,
            "description": "pra_admin_role",
            "value": "arn:aws:iam::<AWS ACCT NUMBER>:role/EC2-Admin,arn:aws:iam::<AWS ACCT NUMBER>:saml-provider/WAAD"
        },
        {
            "allowedMemberTypes": [
                "User"
            ],
            "displayName": "msiam_access",
            "id": "7dfd756e-8c27-4472-b2b7-38c17fc5de5e",
            "isEnabled": true,
            "description": "msiam_access",
            "value": null
        }
    ],
...
```

For more info on the above fields see: <https://msdn.microsoft.com/Library/Azure/Ad/Graph/api/entity-and-complex-type-reference#approle-type>

* Go to the Single Sign on tab and edit the `Role` Attribute. Change the `Value` field to `user.assignedroles`

* Click `Save` on the Single Sign-on blade!

* Go to `Users and Groups` in the Applictation setting and assign roles to the users/groups set up there. Note, you will need to add a user multiple times to give them multiple roles. Thanks AD! :thumbsup:. Alternatively, set up access with just groups and no direct users, then manage user access through the groups.  