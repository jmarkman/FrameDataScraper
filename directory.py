import os
from os import path

class DirectoryNav(object):
    def __init__(self):
        super().__init__()

    def get_home_path(self):
        """Get the current user's home path"""
        return path.expanduser('~')

    def create_directory_at(self, specified_path, new_dir_name, return_new_dir_path=False):
        """Creates a directory with the specified name at the 
        specified path

        Args:
            specified_path: The location where to create the new directory

            new_dir_name: The name of the new directory
            
            return_new_dir_path: Optional parameter. Return new path as string if true.
        Returns:
            If return_new_dir_path is True, return the new path as a string"""
        new_path = path.join(specified_path, new_dir_name)
        if not path.exists(new_path):
            print(f"Creating new directory '{new_dir_name}' at path '{specified_path}'")
            os.makedirs(new_path)
        if return_new_dir_path:
            return new_path