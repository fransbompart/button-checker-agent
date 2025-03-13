from abc import ABC, abstractmethod
import os
from utils.load_json_file import load_json_file
from utils.save_json_file import save_json_file
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from .content_checker_by_section_agent_output import PagesContents, PageContent, PageContentPreviews, PageContentPreview, PageContentMatch, PagesContentsMatches

class ContentCheckerBySectionAgent(ABC):
    def __init__(
            self,
            initialActions: list,
            pageSectionName:str,
            contentType:str,
            previewDetailsPrompt:str,
            agentPath: str,
            api_key: str,
            identifyContentTaskPrompt: str,
            messageContext: str = None,
        ):

        self.initialActions= initialActions
        self.pageSectionName = pageSectionName
        self.contentType = contentType
        self.previewDetailsPrompt = previewDetailsPrompt

        self.identifyContentTaskPrompt = identifyContentTaskPrompt

        self.agentPath = agentPath

        self.browser = Browser(config = BrowserConfig(headless=True)) 

        context = BrowserContext(
            browser = self.browser,
            config = BrowserContextConfig(
                save_recording_path = self.agentPath + '/recordings',
            )
        )

        self.browserContext = context

        self.api_key = api_key

        self.messageContext = messageContext

    async def identify_content_list(self) -> PageContentPreviews:
        controller = Controller(output_model=PageContentPreviews)

        prompt = self.identifyContentTaskPrompt.replace('pageSectionName', self.pageSectionName).replace('previewDetails', self.previewDetailsPrompt).replace('content', self.contentType)

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
        save_json_file(self.agentPath, 'identify_content_agent/result', result)

        if result:
            pageContents: PageContentPreviews = PageContentPreviews.model_validate_json(result)

            for pageContent in pageContents.previews:
                print(pageContent)
                print('---')
            
            return pageContents
        else:
            raise Exception('No Page Contents found')

    @abstractmethod
    async def check_page_content(self, previewDetails: PageContentPreview, previewNumber: int) -> PageContent:
        pass  
    
    def result_to_file(self, fileName: str, result: str):
        directory = os.path.dirname(self.agentPath + '/' + fileName)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.agentPath + '/' + fileName + '.json', 'w') as f:
            f.write(result)

    async def check_previews_vs_pages(self, previews: PageContentPreviews, pages: PagesContents) -> PagesContentsMatches:
        llm = ChatGoogleGenerativeAI(
            model='gemini-1.5-flash',
            api_key=SecretStr(self.api_key),
        )   

        prompt = "In base of the information provided, verify if each of the next previews and pages contents match.\n---\n" 
        
        for i in range(len(previews.previews)):
            preview = previews.previews[i]
            page = pages.pages[i]

            prompt += '{\n' + ' preview: ' + preview.model_dump_json() + '\n page: ' + page.model_dump_json() + '\n}\n'

        print(prompt)

        llmStructured = llm.with_structured_output(PagesContentsMatches)

        response = llmStructured.invoke(prompt)

        return response
        
    async def run(self):
        pagesContentsPreviews = await self.identify_content_list()

        contents = PagesContents(pages=[])

        if pagesContentsPreviews: 
            for i, preview in enumerate(pagesContentsPreviews.previews):
                page = await self.check_page_content(preview, i)        
            
                if page:
                    contents.pages.append(page)
                    
        else:
            raise Exception('No Page Contents found')
        
        save_json_file(self.agentPath, 'check_content_agent/final/previews', pagesContentsPreviews.model_dump_json())
        save_json_file(self.agentPath, 'check_content_agent/final/contents', contents.model_dump_json())

        await self.browser.close()
        await self.browserContext.close()

        previews_data = await load_json_file(self.agentPath + '/check_content_agent/final/previews.json')
        contents_data = await load_json_file(self.agentPath + '/check_content_agent/final/contents.json')

        pagesContentsPreviews = PageContentPreviews.model_validate(previews_data)
        contents = PagesContents.model_validate(contents_data)

        matches = await self.check_previews_vs_pages(pagesContentsPreviews, contents)

        return {
            'matches': matches.model_dump_json(),
            'previews': pagesContentsPreviews.model_dump_json(),
            'contents': contents.model_dump_json()
        }

        


