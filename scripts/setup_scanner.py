# from enum import Enum
# import os
# import asyncio
# import subprocess
# import sys
# from pydantic_settings import BaseSettings


# class SnykCommands(Enum):
#     #continue to add on to this list as needed
#     setup = "setup"
#     scan = "scan"


# class SnykSettings(BaseSettings):
#     """
#     Configuration settings for the application.
#     """
#     SNYK_TOKEN: str | None = None
#     CLIENT_REPO_NAME: str | None = None
#     CLIENT_REPO_URL: str | None = None
#     CLIENT_REPO_PATH: str | None = None
    
    
# class SnykController:
#     def __init__(self, snyk_api_key: str):
#         self.snyk_api_key = snyk_api_key 


#     async def setup_snyk_cli(self):
#         try:
#             subprocess.run(["curl", "-sSL", "https://static.snyk.io/cli/latest/snyk-linux", "-o", "snyk"], check=True)
#             subprocess.run(["chmod", "+x", "./snyk"], check=True)
#             subprocess.run(["sudo", "mv", "./snyk", "/usr/local/bin/"], check=True)
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"Error to setup Snyk CLI: {e}")
#             raise
        

#     async def setup_snyk_api_key(self):
#         try:
#             subprocess.run(["snyk", "config", "set", f"api={self.snyk_api_key}"], check=True)
#             print("Snyk API key set successfully.")
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"Error to setup Snyk API key: {e}")
#             raise
        
        
#     async def validate_Snyk_Cli(self):
#         try:
#             subprocess.run(["snyk", "--version"],check=True)
#             print("Snyk Version Echo Around Action")
#             return True
#         except subprocess.CalledProcessError as e:
#             print(f"Snyk CLI is not installed: {e}")
#             raise
#         except Exception as e:
#             print(f"Error to setup Snyk CLI: {e}")
#             raise 
    
    
# async def run_snyk_scan():
#     try:
#         subprocess.run(["snyk", "code", "test", "--org=d4770938-91e9-454f-b82f-1b4bb72dc30e", "--json"], check=True)
#         return True
#     except Exception as e:
#         print(f"Error to run Snyk scan: {e}")
#         raise


# async def main():
#     try:
#         config = SnykSettings()
#         snyk_client = SnykController(config.SNYK_TOKEN)
#         await snyk_client.setup_snyk_cli()
#         response = await snyk_client.validate_Snyk_Cli()
#         await snyk_client.setup_snyk_api_key()
#         if response:
#             print("Snyk CLI setup successfully.")
#         else:
#             print("Failed to setup Snyk CLI.")
#     except Exception as e:
#         print(f"Error to interface with Snyk client: {e}")
#         return 
    
    
# if __name__ == "__main__":
#     args = sys.argv[1:]
#     command = args[0]
#     assert command in SnykCommands.__members__.keys(), f"Invalid command: {command}"
#     if command == SnykCommands.setup.value:
#         asyncio.run(main())
#     elif command == SnykCommands.scan.value:
#         asyncio.run(run_snyk_scan())

import os
import subprocess
import sys
import asyncio
from enum import Enum
from pydantic_settings import BaseSettings
from subprocess import Popen, PIPE


class SnykCommands(Enum):
    """
    Enum class to define Snyk commands and their current parameters.
    The Commands used here are based off of the assumption the Linux OS is being used.
    Please Update this if you are using a different OS.
    Attributes:
        _setup: Command to setup Snyk CLI.
        _scan: Command to run Snyk scan.
        _snyk_download_script: Command to download Snyk CLI.
        _install_snyk_download_script: Command to install Snyk CLI.
        _move_snyk_download_script: Command to move Snyk CLI to local bin.
        _snyk_version: Command to check Snyk version.
        _snyk_code_scan: Command to run Snyk code scan.
    """
    _setup = "_setup"
    _scan = "_scan"
    _snyk_download_script = ["curl", "-sSL", "https://static.snyk.io/cli/latest/snyk-linux", "-o", "snyk"] 
    _install_snyk_download_script = ["chmod", "+x", "./snyk"]
    _move_snyk_download_script = ["sudo", "mv", "./snyk", "/usr/local/bin/"]
    _snyk_version = ["snyk", "--version"]
    _snyk_code_scan = ["snyk", "code", "test", "--org=d4770938-91e9-454f-b82f-1b4bb72dc30e", "--json"]
    

class SnykSettings(BaseSettings):
    """
    Configuration settings for the application.
    """
    SNYK_TOKEN: str | None = None
    CLIENT_REPO_NAME: str | None = None
    CLIENT_REPO_URL: str | None = None
    CLIENT_REPO_PATH: str | None = None
    
    
class SnykController:
    """
    Class to manage Snyk CLI setup and configuration.
    attr:
        snyk_api_key (str): The Snyk API key.
    methods:
        setup_snyk_cli(): Sets up the Snyk CLI.
        setup_snyk_api_key(): Sets the Snyk API key.
        validate_Snyk_Cli(): Validates the Snyk CLI installation.
    """
    def __init__(self, snyk_api_key: str):
        self.snyk_api_key = snyk_api_key 


    async def setup_snyk_cli(self):
        """
        Sets up the Snyk CLI by downloading and installing it.
        Returns:
            bool: True if setup is successful, False otherwise.
        Raises:
            subprocess.CalledProcessError: If any command fails.
        """
        try:
            download = Popen(
                SnykCommands._snyk_download_script.value,
                stdout=PIPE,
                stderr=PIPE
                )
            stdout, stderr = download.communicate()
            if download.returncode != 0:
                print(f"Error downloading Snyk CLI: {stderr.decode()}")
                raise Exception(f"Error downloading Snyk CLI: {stderr.decode()}") 
            
            install = Popen(
                SnykCommands._install_snyk_download_script.value,
                stdout=PIPE,
                stderr=PIPE
                )
            stdout, stderr = install.communicate()
            if install.returncode != 0:
                print(f"Error installing Snyk CLI: {stderr.decode()}")
                raise Exception(f"Error installing Snyk CLI: {stderr.decode()}")
            
            move = Popen(
                SnykCommands._move_snyk_download_script.value,
                stdout=PIPE,
                stderr=PIPE
                )
            stdout, stderr = move.communicate()
            if move.returncode != 0:
                print(f"Error moving Snyk CLI: {stderr.decode()}")
                raise Exception(f"Error moving Snyk CLI: {stderr.decode()}")
            
            result = {
                "_download_script_": stdout.decode(),
                "_install_script_": stdout.decode(),
                "_move_script_": stdout.decode()
            }
            return result
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        
        except subprocess.CalledProcessError as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise
        
        except Exception as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise
        

    async def setup_snyk_api_key(self):
        """
        Sets the Snyk API key for the CLI.
        Returns:
            bool: True if API key is set successfully, False otherwise.
        Raises:
            subprocess.CalledProcessError: If any command fails.
        """
        try:
            set_api_key = Popen(
                ["snyk", "config", "set", f"api={self.snyk_api_key}"], 
                stdout=PIPE,
                stderr=PIPE
                )
            stdout, stderr = set_api_key.communicate()
            if set_api_key.returncode != 0:
                print(f"Error setting Snyk API key: {stderr.decode()}")
                raise Exception(f"Error setting Snyk API key: {stderr.decode()}")
            return {"set_api_key": stdout.decode()}
        
        except subprocess.CalledProcessError as e:
            print(f"Error to setup Snyk API key: {e}")
            raise
        
        except Exception as e:
            print(f"Error to setup Snyk API key: {e}")
            raise
        
        
    async def validate_Snyk_Cli(self):
        """
        Validates the Snyk CLI installation by checking its version.
        Returns:
            bool: True if Snyk CLI is installed, False otherwise.
        Raises:
            subprocess.CalledProcessError: If any command fails.
        """
        try:
            validation = Popen(
                SnykCommands._snyk_version.value,
                stderr=PIPE,
                stdout=PIPE
                )
            stdout, stderr = validation.communicate()
            if validation.returncode != 0:
                print(f"Error validating Snyk CLI: {stderr.decode()}")
                raise Exception(f"Error validating Snyk CLI: {stderr.decode()}")
            
            return {"snyk_version": stdout.decode()}
        
        except subprocess.CalledProcessError as e:
            print(f"Snyk CLI is not installed: {e}")
            raise
        
        except Exception as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise 
    
    
    @staticmethod
    async def run_snyk_scan():
        """
        Runs the Snyk code scan.
        Returns:
            bool: True if scan is successful, False otherwise.
        Raises:
            subprocess.CalledProcessError: If any command fails.
        """
        try:
            snyk_scan = Popen(
                SnykCommands._snyk_code_scan.value, 
                stdout=PIPE,
                stderr=PIPE
                )
            stdout, stderr = snyk_scan.communicate()
            if snyk_scan.returncode != 0:
                print(f"Error running Snyk scan: {stderr.decode()}")
                raise Exception(f"Error running Snyk scan: {stderr.decode()}")
            return {"snyk_scan": stdout.decode()}

        except subprocess.CalledProcessError as e:
            print(f"Error to run Snyk scan: {e}")
            raise

        except Exception as e:
            print(f"Error to run Snyk scan: {e}")
            raise


async def setup_snyk_scan_cli():
    """
    Sets up the Snyk scan CLI and validates it.
    Returns:
        None
    Raises:
        Exception: If any error occurs during setup or validation.
    """
    try:
        config = SnykSettings()
        snyk_client = SnykController(config.SNYK_TOKEN)
        await snyk_client.setup_snyk_cli()
        response = await snyk_client.validate_Snyk_Cli()
        await snyk_client.setup_snyk_api_key()
        if response:
            print("Snyk CLI setup successfully.")
        else:
            print("Failed to setup Snyk CLI.")
    except Exception as e:
        print(f"Error to interface with Snyk client: {e}")
        return 
    
    
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please provide a command."
    args = sys.argv[1:]
    command = args[0]
    assert command in SnykCommands.__members__.keys(), f"Invalid command: {command}"
    if command == SnykCommands._setup.value:
        asyncio.run(setup_snyk_scan_cli())
    if command == SnykCommands._scan.value:
        asyncio.run(SnykController.run_snyk_scan())
