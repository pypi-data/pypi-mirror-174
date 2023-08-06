from abc import ABC, abstractmethod
from ldap3 import Server, ServerPool, Connection, SAFE_SYNC, RANDOM
from ad_leavers.models.core.object_class import ObjectClass

# > The AD abstract class
# > All object class operations will inherit from this class
# > Authentication is done in constructor
class AdOperations(ABC):
    
    def __init__(self, hosts, username, password) -> None:
        
        # * Create a server pool and add the servers in it
        server_pool = ServerPool([Server(host) for host in hosts], RANDOM)

        # * Create a connection for use
        self.connection = Connection(server_pool, username, password, client_strategy=SAFE_SYNC, auto_bind=True)

    @abstractmethod
    def get_all(self, search_base: str) -> list[ObjectClass]: pass

    @abstractmethod
    def deep_single_search(self, search_base: str, unique_identifier: object) -> ObjectClass: pass

    @abstractmethod
    def move(self, distinguished_name: str, changes: dict) -> None: pass

    @abstractmethod
    def delete(self, distinguished_name: str) -> None: pass

    