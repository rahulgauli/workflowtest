from enum import Enum
import os
import asyncio
import subprocess
import sys
from pydantic_settings import BaseSettings


class SnykCommands(Enum):
    #continue to add on to this list as needed
    setup = "setup"
    scan = "scan"


class SnykSettings(BaseSettings):
    """
    Configuration settings for the application.
    """
    SNYK_TOKEN: str | None = None
    CLIENT_REPO_NAME: str | None = None
    CLIENT_REPO_URL: str | None = None
    CLIENT_REPO_PATH: str | None = None
    
    
class SnykController:
    def __init__(self, snyk_api_key: str):
        self.snyk_api_key = snyk_api_key 


    async def setup_snyk_cli(self):
        try:
            subprocess.run(["curl", "-sSL", "https://static.snyk.io/cli/latest/snyk-linux", "-o", "snyk"], check=True)
            subprocess.run(["chmod", "+x", "./snyk"], check=True)
            subprocess.run(["sudo", "mv", "./snyk", "/usr/local/bin/"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise
        

    async def setup_snyk_api_key(self):
        try:
            subprocess.run(
                ["snyk", "config", "set", f"api={self.snyk_api_key}"],
                check=True
            )
            print("Snyk API key set successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error to setup Snyk API key: {e}")
            raise
        
        
    async def validate_Snyk_Cli(self):
        try:
            result = subprocess.run(
                ["snyk", "--version"],
                check=True
            )
            output = result.stdout.decode("utf-8").strip()
            if not output:
                print("Snyk CLI is not installed.")
                return False
            version = output.split()[1]
            return version
        except subprocess.CalledProcessError as e:
            print(f"Snyk CLI is not installed: {e}")
            raise
        except Exception as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise 
    
    
async def run_snyk_scan():
    try:
        result = subprocess.run(
            ["snyk", "code", "test", "--org=d4770938-91e9-454f-b82f-1b4bb72dc30e", "--json"],
            check=True
        )
        print(f"Snyk scan output: {result}")
        return result
    except Exception as e:
        print(f"Error to run Snyk scan: {e}")
        raise


async def main():
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
    args = sys.argv[1:]
    command = args[0]
    assert command in SnykCommands.__members__.keys(), f"Invalid command: {command}"
    if command == SnykCommands.setup.value:
        asyncio.run(main())
    elif command == SnykCommands.scan.value:
        asyncio.run(run_snyk_scan())
