from ..content_checker_by_section_agent import ContentCheckerBySectionAgent
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from browser_use.agent.views import AgentState
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from ..content_checker_by_section_agent_output import PageContent, PageContentPreviews, PageContentPreview, PagesContents, PagesContentsMatches
from .evaluate_content_prompt import EVALUATE_CONTENT_TASK
from .system_prompt import SYSTEM_PROMPT

class SoyZenContentCheckerBySectionAgent(ContentCheckerBySectionAgent):
    def __init__(
            self,
            initialActions: list,
            pageSectionName:str,
            pageSectionNumber: int,
            previewDetailsPrompt:str,
            contentType:str,
            agentPath: str,
            api_key: str
        ):
        super().__init__(initialActions, pageSectionName, contentType, previewDetailsPrompt, agentPath, api_key, SYSTEM_PROMPT)
        self.pageSectionNumber = pageSectionNumber
        

    async def check_page_content(self, previewDetails: PageContentPreview, previewNumber: int) -> PageContent:
        evaluate_post_controller = Controller(output_model=PageContent)

        @evaluate_post_controller.action('If dialog about Calendario Lunar appears, close it')
        async def close_lunar_calendar_dialog(browser: Browser) -> ActionResult:
            return await close_dialog(browser)

        @evaluate_post_controller.action('Click on the post item')
        async def click_post_item(browser: Browser, postIndex: int) -> ActionResult:
            return await click_post(browser, self.pageSectionNumber, postIndex)
        
        agent = Agent(
            task=EVALUATE_CONTENT_TASK
                .replace('content_preview_title', previewDetails.content_preview_title)
                .replace('previewNumber', str(previewNumber)),
            llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initialActions,
            controller=evaluate_post_controller
        )

        history = await agent.run()
        history.save_to_file(self.agentPath + f'/click_post_item_{previewNumber}/history.json')

        action_description = history.final_result()
        self.result_to_file(f'click_post_item_{previewNumber}/result', action_description)

        return PageContent.model_validate_json(action_description)


async def close_dialog(browser: Browser) -> ActionResult:
    page = await browser.get_current_page()
    try:
        close_button = await page.query_selector('.ct-close-icon')
        if close_button:
            await close_button.click()
            print("Dialog closed")
            return ActionResult(extracted_content='Dialog closed', success=True)
        else:
            print("Didn't find the dialog")
            return ActionResult(extracted_content="Didn't find the dialog", success=False)
    except Exception as e:
        print(f"Error: {e}")
        return ActionResult(extracted_content="Error", success=False)

async def click_post(browser: Browser, pageSectionNumber: int, postIndex: int) -> ActionResult:
    page = await browser.get_current_page()
    url = page.url

    sections = await page.query_selector_all('app-section-home')
    if sections:
        section = sections[pageSectionNumber]
        cards = await section.query_selector_all('.card')
        if cards:
            print(cards[postIndex])
            await cards[postIndex].click()
            await page.wait_for_timeout(2000)
            currentUrl = page.url
            print(f'Current URL: {currentUrl}') 

            if currentUrl != url: 
                print('Clicked on the requested post item')
                return ActionResult(extracted_content='Clicked on the post item and now we are on its page', include_in_memory=True, success=True)
            elif currentUrl == url:
                print('Clicked on the requested post item')
                return ActionResult(extracted_content='Clicked on the post item and the dialog "¡Prueba Gratis 5 días!" appeared', include_in_memory=True, success=True)
            else:
                print('No posts found inside the section')
                return ActionResult(success=False)
        else:
            print('No sections found')
            return ActionResult(success=False)