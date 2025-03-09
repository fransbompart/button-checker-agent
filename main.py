import asyncio
from button_checker_agent.button_checker_agent import ButtonCheckerAgent
from content_checker_by_section_agent.content_checker_by_section_agent import ContentCheckerBySectionAgent
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
    api_key = os.getenv('DEEPSEEK_API_KEY', '')
    print(api_key)
    input('Press Enter to continue...')

    agent = ContentCheckerBySectionAgent(
        initial_actions=[
            {'open_tab': {'url': 'https://vida-fit.com/recetas-fitness/'}},
        ],
        recordings_path='content_checker_by_section_agent/recordings_vida-fit',
        return_page_url='https://vida-fit.com/recetas-fitness/',
        api_key=api_key,
    )

    await agent.run(pageSectionName='"¿Buscas recetas saludables y fáciles? Estás en el sitio indicado"')


async def main():
    load_dotenv()

    # await check_buttons()

    await check_content()


if __name__ == '__main__':
    asyncio.run(main())