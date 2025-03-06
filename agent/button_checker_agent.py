from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from .button_checker_agent_output import ButtonsNamesOutput, ButtonCheckerAgentOutputs
from .task_prompt import STEP_1, STEP_2

class ButtonCheckerAgent():
    def __init__(self):

        self.initial_actions= [{'open_tab': {'url': 'https://soyzen.com/home'}}]

        # self.controller = agentController.controller
        
        context = BrowserContext(
            browser = Browser(config = BrowserConfig(headless=True)),
            config = BrowserContextConfig(
                save_recording_path ='recordings_2',
                browser_window_size = {'width': 1280, 'height': 500},
            )
        )

        self.browserContext = context

        self.firts_agent_history = []
        self.second_agent_history = []


    async def run_firts_agent(self, prompt: str) -> ButtonsNamesOutput:
        firts_agent = Agent(
            task=prompt,
            llm=ChatOpenAI(model='gpt-4o'),
            browser_context=self.browserContext,
            initial_actions=self.initial_actions,
            controller=Controller(output_model=ButtonsNamesOutput),
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
            await page.goto('https://soyzen.com/home')
            
            print('Returned to the original previous page')
            return ActionResult(extracted_content='Returned to the original previous page')

        second_agent = Agent(
            task=prompt,
            llm=ChatOpenAI(model='gpt-4o'),
            browser_context=self.browserContext,
            initial_actions=self.initial_actions,
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
        else:
            raise Exception('No buttons found')


    async def check(self):
        buttons_names = await self.run_firts_agent(prompt=STEP_1)

        print(f'Buttons found: {buttons_names}')

        prompt = STEP_2 + '\n'.join([f"- {button_name}" for button_name in buttons_names])

        buttons_output = await self.run_second_agent(prompt=prompt)

        print(f'Buttons output: {buttons_output.outputs}')

        await self.run_second_agent()

        await self.browserContext.close()
        await self.browser.close()
        

        


