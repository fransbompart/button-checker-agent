import os
from content_checker_by_section_agent.soyZen.soy_zen_content_checker_by_section_agent import SoyZenContentCheckerBySectionAgent
from content_checker_by_section_agent.vidaFit.vida_fit_content_checker_by_section_agent import VidaFitContentCheckerBySectionAgent

class ContentCheckerAgentRunner:
    @staticmethod
    async def run(app: str):
        api_key = os.getenv('GEMINI_API_KEY', '')

        if app == "SoyZen":
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
            
        elif app == "VidaFit":
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
        else:
            raise ValueError("Invalid app")
        
        return await agent.run()