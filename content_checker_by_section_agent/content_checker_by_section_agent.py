from abc import ABC, abstractmethod

from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from .identify_content_prompt import IDENTIFY_CONTENT_TASK
from .content_checker_by_section_agent_output import PageContentPreviews, PageContentPreview, PageContentMatch, PagesContentsMatches

class ContentCheckerBySectionAgent(ABC):
    def __init__(
            self,
            initialActions: list,
            pageSectionName:str,
            contentType:str,
            previewDetailsPrompt:str,
            agentPath: str,
            api_key: str,
            messageContext: str = None,):

        self.initialActions= initialActions
        self.pageSectionName = pageSectionName
        self.contentType = contentType
        self.previewDetailsPrompt = previewDetailsPrompt

        self.agentPath = agentPath

        context = BrowserContext(
            browser = Browser(config = BrowserConfig(headless=True)),
            config = BrowserContextConfig(
                save_recording_path = self.agentPath + '/recordings',
            )
        )

        self.browserContext = context

        self.api_key = api_key

        self.messageContext = messageContext

    async def identify_content_list(self) -> PageContentPreviews:
        controller = Controller(output_model=PageContentPreviews)

        prompt = IDENTIFY_CONTENT_TASK.replace('pageSectionName', self.pageSectionName).replace('previewDetails', self.previewDetailsPrompt).replace('content', self.contentType)
                
        prompt = f"## System Context\n{self.messageContext}\n---\n## Task\n{prompt}"
        print(prompt)

        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initialActions,
            controller=controller,
        )

        identify_content_agent_history = await agent.run()
        
        identify_content_agent_history.save_to_file(self.agentPath + '/identify_content_agent/history.json')

        result = identify_content_agent_history.final_result()

        if result:
            pageContents: PageContentPreviews = PageContentPreviews.model_validate_json(result)

            for pageContent in pageContents.previews:
                print(pageContent)
            
            return pageContents
        else:
            raise Exception('No Page Contents found')

    @abstractmethod
    async def check_page_content(self, previewDetails: PageContentPreview) -> PageContentMatch:
        pass        
        
    async def run(self) -> PagesContentsMatches:
        pagesContentsPreviews = await self.identify_content_list()

        pagesContentsMatches = PagesContentsMatches(contents=[])

        if pagesContentsPreviews: 
            for preview in pagesContentsPreviews.previews[:3]:
                pageContentMatch = await self.check_page_content(preview)        
            
                if pageContentMatch:
                    pagesContentsMatches.contents.append(pageContentMatch)
        else:
            raise Exception('No Page Contents found')
        
        await self.browserContext.close()
        return pagesContentsMatches

        


