from content_checker_by_section_agent.content_checker_by_section_agent import ContentCheckerBySectionAgent
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from content_checker_by_section_agent_output import PageContentPreviews, PageContentPreview, PageContentMatch, PagesContentsMatches
from evaluate_content_prompt import EVALUATE_CONTENT_TASK

class VidaFitContentCheckerBySectionAgent(ContentCheckerBySectionAgent):
    def __init__(self, initialActions: list, pageSectionName:str, contentType:str, previewDetailsPrompt:str, agentPath: str, api_key: str):
        super().__init__(initialActions, pageSectionName, contentType, previewDetailsPrompt, agentPath, api_key)
    
    async def check_page_content(self, previewDetails: PageContentPreview) -> PageContentMatch:
        controller = Controller(output_model=PageContentMatch)

        @controller.action('Click on recipe item')
        async def click_recipe_item(browser: Browser, pageUrl: str) -> ActionResult:
            page = await browser.get_current_page()

            element = await page.query_selector(f'a[href="{pageUrl}"]')
            if element:
                await element.click()
                return ActionResult(success=True)

        details = [
            f'- Title: {previewDetails.content_preview_title}',
            f'- Categories: {previewDetails.content_preview_categories}',
            f'- Page URL: {previewDetails.content_page_url}',
        ]
        
        prompt = (EVALUATE_CONTENT_TASK
                  .replace('pageSectionName', self.pageSectionName)
                  .replace('contentPreviewTitle', previewDetails.content_preview_title) 
                ) + '\n'.join(details)

        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initial_actions,
            controller=controller,
        )

        check_content_agent_history = await agent.run()
        check_content_agent_history.save_to_file(self.agentPath + '/check_content_agent/history.json')

        result = check_content_agent_history.final_result()
        if result:
            pageContentMatch: PageContentMatch = PageContentMatch.model_validate_json(result)

            print(pageContentMatch)
            
            return pageContentMatch
        else:
            raise Exception('No Page Contents found')
