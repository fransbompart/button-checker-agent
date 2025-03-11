import asyncio
from button_checker_agent.button_checker_agent import ButtonCheckerAgent
from content_checker_by_section_agent.soyZen.soy_zen_content_checker_by_section_agent import SoyZenContentCheckerBySectionAgent
from content_checker_by_section_agent.vidaFit.vida_fit_content_checker_by_section_agent import VidaFitContentCheckerBySectionAgent
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

async def check_content_soy_zen():
    api_key = os.getenv('GEMINI_API_KEY', '')

    previewDetailsPrompt = """
    - `content_preview_title`: The title of the content.
    - `content_preview_categories`: The categories of the content (if avaible).
    - `content_preview_type`: The type of the content, can be a Audio/Video or Blog.
    - `public_access`: False if item has a Padlock Icon on one border, else True.
    - `content_preview_duration`: The duration of the content (if available).
    """

    agent = SoyZenContentCheckerBySectionAgent(
        initialActions = [
            {'open_tab': {'url': 'https://soyzen.com/home'}},
        ],
        pageSectionName = 'Mood Zen del día',
        previewDetailsPrompt= previewDetailsPrompt,
        pageSectionNumber = 0,
        contentType = 'post',
        agentPath = 'content_checker_by_section_agent/soyZen',
        api_key = api_key,
    )

    await agent.run()

async def check_content_vida_fit():
    api_key = os.getenv('GEMINI_API_KEY', '')
    
    previewDetailsPrompt = """
    - `content_preview_title`
    - `content_preview_categories`
    """

    agent = VidaFitContentCheckerBySectionAgent(
        initialActions = [
            {'open_tab': {'url': 'https://vida-fit.com/recetas-fitness/'}},
        ],
        pageSectionName = '¿Buscas recetas saludables y fáciles? Estás en el sitio indicado',
        previewDetailsPrompt= previewDetailsPrompt,
        contentType = 'recipe',
        agentPath = 'content_checker_by_section_agent/vidaFit',
        api_key = api_key,
    )

    await agent.run()


async def main():
    load_dotenv()

    Laminar.initialize(project_api_key=os.getenv('LMNR_PROJECT_API_KEY', ''))

    # await check_buttons()

    # await check_content_vida_fit()
    await check_content_soy_zen()


if __name__ == '__main__':
    asyncio.run(main())