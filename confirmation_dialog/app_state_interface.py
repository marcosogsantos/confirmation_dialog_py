from typing import Protocol, runtime_checkable

@runtime_checkable
class AppStateInterface(Protocol):
    """Interface for app state objects that can store key-value pairs."""
    
    def set(self, key: str, value: any) -> None:
        """
        Store a value with the given key.
        
        :param key: The key to store the value under
        :param value: The value to store
        """
        ... 