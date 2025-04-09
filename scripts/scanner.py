import os
import asyncio
import subprocess
from pydantic_settings import BaseSettings


class SnykController:
    def __init__(self, snyk_api_key: str):
        self.snyk_api_key = snyk_api_key 

#curl https://static.snyk.io/cli/latest/snyk-linux -o snyk
#chmod +x ./snyk
#mv ./snyk /usr/local/bin/ 


    async def setup_snyk_cli(self):
        try:
            subprocess.run(["curl", "-sSL", "https://static.snyk.io/cli/latest/snyk-linux", "-o", "snyk"], check=True)
            subprocess.run(["chmod", "+x", "./snyk"], check=True)
            subprocess.run(["sudo", "mv", "./snyk", "/usr/local/bin/"], check=True)
            # subprocess.run([
            #     "sudo", "apt-get", "install", "-y", "npm"
            # ], check=True)
            # subprocess.run(
            #     ["npm", "install", "-g", "snyk"],
            #     check=True
            # )
        except subprocess.CalledProcessError as e:
            print(f"Error to setup Snyk CLI: {e}")
            raise
        
        
    async def setup_snyk_api_key(self):
        try:
            # Set Snyk API key
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
            # Check if Snyk CLI is installed
            result = subprocess.run(
                ["snyk", "--version"],
                check=True
            )
            print(f"Snyk CLI version: {result}")
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
    SNYK_TOKEN: str | None = None
    CLIENT_REPO_NAME: str | None = None
    CLIENT_REPO_URL: str | None = None
    CLIENT_REPO_PATH: str | None = None


async def main():
    try:
        config = SnykSettings()
        snyk_client = SnykController(config.SNYK_TOKEN)
        await snyk_client.setup_snyk_cli()
        response = await snyk_client.validate_Snyk_Cli()
        await snyk_client.setup_snyk_api_key()
        # Validate Snyk CLI
        if response:
            print("Snyk CLI is installed and validated.")
            response = await snyk_client.run_snyk_scan()
        else:
            print("Snyk CLI validation failed.")
        if response:
            print("Snyk CLI setup successfully.")
        else:
            print("Failed to setup Snyk CLI.")
    except Exception as e:
        print(f"Error to interface with Snyk client: {e}")
        return
    
if __name__ == "__main__":
    asyncio.run(main())
