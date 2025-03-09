from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from .content_checker_by_section_agent_output import PageContentMatch, PagesContentsMatches, PageContentPreview, PageContentPreviews  
from .task_prompt import IDENTIFY_CONTENT_TASK, EVALUATE_CONTENT_TASK

class ContentCheckerBySectionAgent:
    def __init__(self, initial_actions: list, return_page_url:str, recordings_path: str, api_key: str):

        self.initial_actions= initial_actions
        self.return_page_url = return_page_url

        context = BrowserContext(
            browser = Browser(config = BrowserConfig(headless=True)),
            config = BrowserContextConfig(
                save_recording_path = recordings_path,
            )
        )

        self.browserContext = context

        self.identify_content_agent_history = []
        self.check_content_agent_history = []

        self.llm = ChatDeepSeek(
            model="deepseek-chat",
        )

    async def identify_content_list(self, pageSectionName: str) -> PageContentPreviews:
        controller = Controller(output_model=PageContentPreviews)

        agent = Agent(
            task=IDENTIFY_CONTENT_TASK.replace('pageSectionName', pageSectionName),
            llm=self.llm,
            browser_context=self.browserContext,
            initial_actions=self.initial_actions,
            controller=controller,
        )

        self.identify_content_agent_history = await agent.run()

        result = self.identify_content_agent_history.final_result()

        if result:
            pageContents: PageContentPreviews = PageContentPreviews.model_validate_json(result)

            for pageContent in pageContents.previews:
                print(pageContent)
            
            return pageContents
        else:
            raise Exception('No Page Contents found')


    async def check_page_content(self, pageSectionName: str) -> PageContentMatch:
        controller = Controller(output_model=PageContentMatch)

        agent = Agent(
            task=EVALUATE_CONTENT_TASK.replace('pageSectionName', pageSectionName),
            llm=ChatOpenAI(model='gpt-4o'),
            browser_context=self.browserContext,

            controller=controller,
        )

        self.check_content_agent_history = await agent.run()

        result = self.check_content_agent_history.final_result()
        if result:
            pageContents: PageContentMatch = PageContentMatch.model_validate_json(result)

            for pageContent in pageContents.contents:
                print(pageContent)
            
            return pageContents
        else:
            raise Exception('No Page Contents found')
        
        
    async def run(self, pageSectionName: str) -> PagesContentsMatches:
        pagesContentsPreviews = await self.identify_content_list(pageSectionName)

        await self.browserContext.close()

        


