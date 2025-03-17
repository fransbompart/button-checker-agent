from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from .button_checker_agent_output import ButtonsNamesOutput, ButtonCheckerAgentOutputs
from .task_prompt import STEP_1, STEP_2
from pydantic import SecretStr

class ButtonCheckerAgent():
    def __init__(self, initial_actions: list, return_page_url:str, browser_window_size: dict, api_key: str):

        self.initial_actions= initial_actions
        self.return_page_url = return_page_url
        self.api_key = api_key

        self.browser = Browser(config = BrowserConfig(headless=True)) 

        context = BrowserContext(
            browser = self.browser,
            config = BrowserContextConfig(
                browser_window_size = browser_window_size,
            )
        )

        self.browserContext = context

        self.firts_agent_history = []
        self.second_agent_history = []

    async def run_close_dialog_agent(self):
        close_dialog_agent = Agent(
            task="If a dialog about Calendario Lunar appears, close it.\n###Important\n- Don't scroll.",
            llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initial_actions,
            controller=Controller()
        )

        await close_dialog_agent.run()
        
        

    async def run_firts_agent(self, prompt: str) -> ButtonsNamesOutput:

        firstAgentController=Controller(output_model=ButtonsNamesOutput)

        # @firstAgentController.action('If a dialog appears, close it')
        # async def close_dialog(browser: Browser):
        #     page = await browser.get_current_page()
        #     close_button = await page.query_selector('[svgicon="cancel_icon"]')
        #     if close_button:
        #         await close_button.click()
        #         print('Closed the dialog')
        #         return ActionResult(extracted_content='Closed the dialog')
        #     else:
        #         print('Close button not found')
        #         return ActionResult(extracted_content='Close button not found')

        firts_agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            # planner_llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            # initial_actions=self.initial_actions,
            controller=firstAgentController,
        )

        self.firts_agent_history = await firts_agent.run()

        result = self.firts_agent_history.final_result()

        if result:
            buttons: ButtonsNamesOutput = ButtonsNamesOutput.model_validate_json(result)

            for button_name in buttons:
                print(f'Button Name: {button_name}')

                return buttons
        else:
            raise Exception('No buttons found')
        

    async def run_second_agent(self, prompt: str):
        secondAgentController=Controller(output_model=ButtonCheckerAgentOutputs)

        @secondAgentController.action('If clicking an element navigates to a new page, return to the previous one')
        async def return_to_previous_page(browser: Browser):
            page = await browser.get_current_page()
            await page.goto(self.return_page_url)
            
            print('Returned to the original previous page')
            return ActionResult(extracted_content='Returned to the original previous page')

        second_agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            # planner_llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            # initial_actions=self.initial_actions,
            controller=secondAgentController,
        )

        self.second_agent_history = await second_agent.run()

        result = self.second_agent_history.final_result()

        if result:
            buttons: ButtonCheckerAgentOutputs = ButtonCheckerAgentOutputs.model_validate_json(result)

            for button in buttons.outputs:
                print(f'Button Name: {button.button_name}')
                print(f'Button Action Result Description: {button.button_action_result_description}')
                print(f'Button Action Result Success: {button.button_action_result_success}')
            
            return buttons
        else:
            raise Exception('No buttons found')
        

    async def check(self) -> ButtonCheckerAgentOutputs:
        await self.run_close_dialog_agent()
        print('Dialog closed')

        buttons_names = await self.run_firts_agent(prompt=STEP_1)

        buttons_names = '\n'.join([f"- {button_name}" for button_name in buttons_names.button_name])

        print(f'Buttons found: {buttons_names}')
        input()

        prompt = STEP_2 + '\n' + buttons_names

        buttons_output = await self.run_second_agent(prompt=prompt)

        print(f'Buttons output: {buttons_output.outputs}')

        await self.browser.close()
        await self.browserContext.close()

        return buttons_names
        

        


