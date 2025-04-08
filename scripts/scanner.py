import os
import asyncio
import subprocess
from pydantic_settings import BaseSettings


class SnykController:
    def __init__(self, snyk_api_key: str):
        self.snyk_api_key = snyk_api_key 

        
    async def validate_Snyk_Cli(self):
        try:
            # Check if Snyk CLI is installed
            result = subprocess.run(
                ["snyk", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            version = result.stdout.decode("utf-8").strip()
            print(f"Snyk CLI version: {version}")
            return True
        except Exception as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise 
    
    async def run_snyk_scan(self):
        try:
            # Run Snyk scan command
            result = subprocess.run(
                ["snyk", "test"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            output = result.stdout.decode("utf-8").strip()
            print(f"Snyk scan output: {output}")
            return True
        except Exception as e:
            print(f"Error to run Snyk scan: {e}")
            raise

class SnykSettings(BaseSettings):
    """
    Configuration settings for the application.
    """
    SNYK_TOKEN: str
    CLIENT_REPO_NAME: str
    CLIENT_REPO_URL: str
    CLIENT_REPO_PATH: str


async def main():
    try:
        config = SnykSettings()
        snyk_client = SnykController(config.SNYK_TOKEN)
        response = await snyk_client.validate_Snyk_Cli()
        scan_result = await snyk_client.run_snyk_scan()
        
        if response:
            print("Snyk CLI setup successfully.")
        else:
            print("Failed to setup Snyk CLI.")
    except Exception as e:
        print(f"Error to interface with Snyk client: {e}")
        return
    
if __name__ == "__main__":
    asyncio.run(main())
    
