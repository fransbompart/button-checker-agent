import asyncio
from lmnr import Laminar
from dotenv import load_dotenv
import os

from content_checker_by_section_agent.content_checker_by_section_agent_runner import ContentCheckerAgentRunner

from button_checker_agent.button_checker_agent import ButtonCheckerAgent

from content_checker_by_section_agent.soyZen.soy_zen_content_checker_by_section_agent import SoyZenContentCheckerBySectionAgent
from content_checker_by_section_agent.vidaFit.vida_fit_content_checker_by_section_agent import VidaFitContentCheckerBySectionAgent


async def check_buttons():
    agent = ButtonCheckerAgent(
        initial_actions=[
            {'open_tab': {'url': 'https://aqustico.com/home'}},
        ],
        recordings_path='button_checker_agent/recordings_aqustico',
        return_page_url='https://aqustico.com/home',
        browser_window_size={'width': 1280, 'height': 500}
    )

    await agent.check()

async def check_content_soy_zen():
    content_output = await ContentCheckerAgentRunner.run("SoyZen")

    print(content_output)
    
async def check_content_vida_fit():
    content_output = await ContentCheckerAgentRunner.run("VidaFit")

    print(content_output)

async def main():
    load_dotenv()

    Laminar.initialize(project_api_key=os.getenv('LMNR_PROJECT_API_KEY', ''))

    # await check_buttons()

    # await check_content_vida_fit()
    await check_content_soy_zen()


if __name__ == '__main__':
    asyncio.run(main())