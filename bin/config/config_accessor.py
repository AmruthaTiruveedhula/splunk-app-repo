import os

class ConfigAccessor:

    def get_splunk_launch_conf_value(self, key):
        """
        Get the value associated with the specified key from the dot_env_file.

        Parameters:
        - key (str): The key to look up in the configuration.

        Returns:
        - str or None: The value associated with the key, or None if the key is not found.
        """
        # Construct the path to the .env file in the default directory
        dot_env_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..", "default", ".env")

        # Read the .env file and look for the specified key
        with open(dot_env_path, "r") as conf_file:
            for line in conf_file:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=")[1].strip()

        # Return None if the key is not found
        return None
