from ..content_checker_by_section_agent import ContentCheckerBySectionAgent
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from browser_use.agent.views import AgentState
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from ..content_checker_by_section_agent_output import CheckContentOutput, PageContentPreviews, PageContentPreview, PageContentMatch, PagesContentsMatches
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

    async def check_page_content(self, previewDetails: PageContentPreview) -> PageContentMatch:
        pass
        
    def result_to_file(self, fileName: str, result: str):
        with open(self.agentPath + '/' + fileName +'.txt', 'w') as f:
            f.write(result)

    def update_agent_state(self, agent_state: AgentState) -> AgentState:
        agent_state.history.history = []
        
        with open('agent_state.json', 'w') as f:
            serialized = agent_state.model_dump_json(exclude={'history'})
            f.write(serialized)
            
        with open('agent_state.json', 'r') as f:
            loaded_json = f.read()
            agent_state = AgentState.model_validate_json(loaded_json)

        return agent_state

    async def check_section(self):
        identify_post_controller = Controller(output_model=PageContentPreview)

        @identify_post_controller.action('If dialog about Calendario Lunar appears, close it')
        async def close_lunar_calendar_dialog(browser: Browser) -> ActionResult:
            return await close_dialog(browser)

        evaluate_post_controller = Controller(output_model=CheckContentOutput)

        @evaluate_post_controller.action('If dialog about Calendario Lunar appears, close it')
        async def close_lunar_calendar_dialog(browser: Browser) -> ActionResult:
            return await close_dialog(browser)

        @evaluate_post_controller.action('Click on the post item')
        async def click_post_item(browser: Browser, postIndex: int) -> ActionResult:
            return await click_post(browser, self.pageSectionNumber, postIndex)
        
        for i in range(1, 5):
            agent = Agent(
                task=f"""Find the section "{self.pageSectionName}" in the page. Then extract all the information about the post item number {i} that is **UNDER the "{self.pageSectionName}" section**. 
                ---
                **Important:**
                - First, If a dialog with Calendario Lunar appears, **close it before continue**.
                """,
                llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
                browser_context=self.browserContext,
                controller=identify_post_controller,
                initial_actions=self.initialActions,
                message_context=SYSTEM_PROMPT
            )

            preview_history = await agent.run()
            preview_history.save_to_file(self.agentPath + f'/preview_{i}/history.json')

            preview_description = preview_history.final_result()
            self.result_to_file(f'preview_{i}/preview', preview_description)

            secondAgent = Agent(
                task=f"""Identify the post item number {i} that is **UNDER the "{self.pageSectionName}" section**.
                Click on the post item mentioned using the custom function click_post_item.
                Then, if you are in the post page, **extract** and describe the whole post page. Else, if a dialog with message "¡Prueba Gratis 5 días!" appers, say it and end the task successfully.
                
                ---
                
                **Important:**
                - First, If a dialog with Calendario Lunar appears, **close it before continue**.
                """,
                llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
                browser_context=self.browserContext,
                controller=evaluate_post_controller
            )

            history = await secondAgent.run()
            history.save_to_file(self.agentPath + f'/click_post_item_{i}/history.json')

            action_description = history.final_result()
            self.result_to_file(f'click_post_item_{i}/result', action_description)

        await self.browserContext.close()


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
            await cards[postIndex-1].click()
            await page.wait_for_timeout(2000)
            currentUrl = page.url
            print(f'Current URL: {currentUrl}') 

            if currentUrl != url: 
                print('Clicked on the requested post item')
                return ActionResult(extracted_content='Clicked on the post item, is Public', include_in_memory=True, success=True)
            elif currentUrl == url:
                print('Clicked on the requested post item')
                return ActionResult(extracted_content='Clicked on the post item, is Subscribers-Only', include_in_memory=True, success=True)
            else:
                print('No posts found inside the section')
                return ActionResult(success=False)
        else:
            print('No sections found')
            return ActionResult(success=False)