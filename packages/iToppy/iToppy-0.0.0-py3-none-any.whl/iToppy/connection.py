"""The iTop connection object."""
import json
import requests
class iTop:
    """
    Stores connection and session information for the iTop Rest API
    """
    def __init__(
        self, 
        url: str,
        username: str, 
        password: str, 
        verify: bool = True,
        timeout: int = 10
    ):
        pass

    def __str__(self):
        return self.some_key

    def get_x_times(self, x: int):
        """
        Returns the class value X times.

        Args:
            x (int): How many times to return

        Returns:
            str: The class value some_key X times
        """
        return "".join([self.some_key for _ in range(x)])
