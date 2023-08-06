from datetime import datetime
from ldap3 import ALL_ATTRIBUTES, MODIFY_REPLACE
from ad_leavers.models.core.ad_ops import AdOperations
from ad_leavers.models.core.exceptions import AdSearchException, AdModifyException
from ad_leavers.models.core.object_class import ObjectClass
from ad_leavers.models.data_classes.user import User

# > This is the UserOps class that will work with the User dataclass
# > It inherits the AdOperations base class for operations
class UserOps(AdOperations):

    # FIXME(Make sure to call escape_filter_chars() from ldap3.utils.conv on any user input before placing it into a .search() call. This is to avoid possible injection of malicious code. Look at https://www.linkedin.com/pulse/ldap-injection-django-jerin-jose for more information.)

    def __init__(self, hosts, username, password) -> None: 
        
        # * Set the object type
        self.object_class_type = '(objectclass=user)'

        # * Initialize the parent class
        super().__init__(hosts, username, password)
    
    # > Inherited methods from Parent abstract class
    def get_all(self, search_base: str) -> list[User]: 
        
        # * Make API call
        status, _, response, _ = self.connection.search(
            search_base=search_base,
            search_filter=self.object_class_type,
            attributes=ALL_ATTRIBUTES
        )

        if not status: raise AdSearchException(f"Error while searching the searchbase: {search_base}")

        # * Return the schema in the ObjectClass model format
        return [User(schema=schema) for schema in response]

    def deep_single_search(self, search_base: str, unique_identifier: object) -> ObjectClass: 

        # * Construct filter that will perform the deep search
        search_filter = f"""
        (|(mail={unique_identifier})
        (sAMAccountName={unique_identifier.split('@')[0] if '@' in unique_identifier else unique_identifier})
        (cn={unique_identifier.replace('.', ' ')}))
        """

        # * Make API call
        status, result, response, _ = self.connection.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=ALL_ATTRIBUTES
        )

        if not status: raise AdSearchException(f"Error while searching for: {unique_identifier} in {search_base}")

        # * Get the users obtained
        users = [User(schema=schema) for schema in response]

        # * Return the user if it's found
        return users[0] if len(users) != 0 else None 
    
    def delete(self, distinguished_name: str) -> None: 
        
        # * Delete the dn
        result, _, _, _  = self.connection.delete(distinguished_name)

        if not result: raise AdModifyException(f"Error while deleting {distinguished_name}")

    def move(self, distinguished_name: str, cn:str, new_ou: dict) -> None: 
        
        # * Modify the DN
        result, _, _, _  = self.connection.modify_dn(distinguished_name, f'cn={cn}', new_superior=new_ou)

        if not result: raise AdModifyException(f"Error while moving {distinguished_name}")


    # > Unique class methods
    def set_expiration(self, distinguished_name: str, expiration_date: datetime):
        
        # * Set the expiration date
        result, _, _, _ = self.connection.modify(
            distinguished_name,
            {
                'accountExpires': [(MODIFY_REPLACE, [expiration_date])]
            }
        ) 

        if not result: raise AdModifyException(f"Error while setting an expiration date on {distinguished_name}")

    def disable(self, distinguished_name: str):
        # * Disable the account
        result, _, _, _ = self.connection.modify(
            distinguished_name,
            {
                'userAccountControl': [(MODIFY_REPLACE, [514])]
            }
        ) 

        if not result: raise AdModifyException(f"Error while disabling account on {distinguished_name}")