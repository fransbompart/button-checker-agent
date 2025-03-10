import asyncio
from button_checker_agent.button_checker_agent import ButtonCheckerAgent
from content_checker_by_section_agent.soyZen.soy_zen_content_checker_by_section_agent import SoyZenContentCheckerBySectionAgent
from lmnr import Laminar
from dotenv import load_dotenv
import os

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

async def check_content():
    api_key = os.getenv('OPENAI_API_KEY', '')
    print(api_key)

    previewDetailsPrompt = """
    - `content_preview_title`: The title of the content.
    - `content_preview_categories`: The categories of the content (if avaible).
    - `content_page_url`: The URL of the content page.
    - `content_preview_type`: The type of the content, can be a Audio/Video or Blog.
    - `public_access`: False if item has a Padlock Icon on one border, else True.
    - `content_preview_duration`: The duration of the content (if available).
    - `content_preview_index`: The index of the content in the slider of the section, could be 0, 1, 2, ..., **ALWAYS START COUNTING FROM ZERO!!!.**
    """

    agent = SoyZenContentCheckerBySectionAgent(
        initialActions = [
            {'open_tab': {'url': 'https://soyzen.com/home'}},
            {'scroll_down': {'amount': 2000}},
        ],
        pageSectionName = 'Yoga Zen',
        previewDetailsPrompt= previewDetailsPrompt,
        pageSectionNumber = 2,
        contentType = 'post',
        agentPath = 'content_checker_by_section_agent/soyZen',
        api_key = api_key,
    )

    await agent.check_section()


async def main():
    load_dotenv()

    Laminar.initialize(project_api_key=os.getenv('LMNR_PROJECT_API_KEY', ''))

    # await check_buttons()

    await check_content()


if __name__ == '__main__':
    asyncio.run(main())