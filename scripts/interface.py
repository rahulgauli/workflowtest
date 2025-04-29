import asyncio
from http.client import HTTPException 
from httpx import AsyncClient
from pydantic_settings import BaseSettings, SettingsConfigDict

hihi
class InputVariablesFromRunner(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    github_reponame : str
    github_context: str | None = None 
    # github_context this will be later utilized to create a metadata object
    # to track back and create reminders for the user to check the snyk report
    # create Pull Request Comments 
    # create Issues
    # create Actions to store integrate findings to Snyk and tag them to the Repository
    # Create Actions to enable emailing services to notify the user about the findings
    # etc ... Example of the Github_Context is 
    # https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    github_token : str 
    snyk_api_token : str
    snyk_base_url : str
    
class SnykController:
    def __init__(self, config: AppConfig):
        self.config = config
        self.snyk_api_token = config.snyk_api_token
        self.github_token = config.github_token
        self.snyk_base_url = config.snyk_base_url

class GitGuardianController:
    def __init__(self, config: AppConfig):
        self.config = config
        self.gitGuardian_api_token = config.gitGuardian_api_token
        self.github_token = config.github_token
        self.gitguardian_base_url = config.gitguardian_base_url
        
class WizController:
    def __init__(self, config: AppConfig):
        self.config = config
        self.wiz_api_token = config.wiz_api_token
        self.github_token = config.github_token
        self.wiz_base_url = config.wiz_base_url

async def scan_interface():
    try:
        # findings = interface Snyk, GitGuardian and Wiz Scans
        # await enforce custom_policy
        # await notification_services()
        # await publish_findings()
    except Exception as e:
        raise 


    # async def snyk_api_POC(self):
    #     try:
    #         headers = {
    #             "Content-Type": "application/vnd.api+json",
    #             "Authorization": f"token {self.snyk_api_token}"
    #         }
    #         async with AsyncClient() as client:
    #             response = await client.get(
    #                 url=f"{self.snyk_base_url}/rest/orgs",
    #                 headers=headers
    #             )
    #             if response.status_code == 200:
    #                 print(response.json())
    #                 return response.json()
    #             return
    #     except HTTPException as e:
    #         print(e)
    #         raise
    
    #     except Exception as e:
    #         print(e)
    #         raise
            

# controller = SnykController(AppConfig())
# controller.print_config()
if __name__ == "__main__":
    config = AppConfig()
    
    controller = SnykController(config, "https://snyk.io/api/v1")
    response = asyncio.run(controller.snyk_api_POC())
