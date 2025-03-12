from content_checker_by_section_agent.content_checker_by_section_agent import ContentCheckerBySectionAgent
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from ..content_checker_by_section_agent_output import PageContentPreviews, PageContentPreview, PageContent, PagesContentsMatches
from .prompts import IDENTIFY_CONTENT_TASK_VIDA_FIT, EVALUATE_CONTENT_TASK 

class VidaFitContentCheckerBySectionAgent(ContentCheckerBySectionAgent):
    def __init__(
            self,
            initialActions: list,
            pageSectionName: str,
            contentType: str,
            previewDetailsPrompt: str,
            agentPath: str,
            api_key: str,
        ):
        super().__init__(
            initialActions,
            pageSectionName,
            contentType,
            previewDetailsPrompt,
            agentPath,
            api_key,
            IDENTIFY_CONTENT_TASK_VIDA_FIT,
        )


    async def check_page_content(self, previewDetails: PageContentPreview, previewNumber:int) -> PageContent:
        controller = Controller(output_model=PageContent)

        @controller.action('Click recipe item')
        async def click_recipe_item(browser: Browser, pageUrl: str) -> ActionResult:
            page = await browser.get_current_page()

            element = await page.query_selector(f'a[href="{pageUrl}"]')
            if element:
                await element.click()
                return ActionResult(extracted_content='Clicked on the recipe and now I am in the article page', success=True)

        details = [
            f'- Title: {previewDetails.content_preview_title}',
            f'- Categories: {previewDetails.content_preview_categories}',
        ]
        
        prompt = (EVALUATE_CONTENT_TASK
                  .replace('pageSectionName', self.pageSectionName)
                  .replace('contentPreviewTitle', previewDetails.content_preview_title) 
                )
        # + '\n'.join(details)

        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initialActions,
            controller=controller,
        )

        check_content_agent_history = await agent.run()
        check_content_agent_history.save_to_file(self.agentPath + '/check_content_agent/history.json')
        
        result = check_content_agent_history.final_result()

        self.result_to_file(f'click_post_item_{previewNumber}/result', result)

        if result:
            pagesContents: PageContent = PageContent.model_validate_json(result)

            print(pagesContents)
            
            return pagesContents
        else:
            raise Exception('No Page Contents found')
