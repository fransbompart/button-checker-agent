from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from .button_checker_agent_output import ButtonsNamesOutput, ButtonCheckerAgentOutputs
from .task_prompt import STEP, STEP_1, STEP_2

class ButtonCheckerAgent():
    def __init__(self):

        self.initial_actions= [{
            'open_tab': {'url': 'https://aqustico.com/home'},
            'scroll_down': {'amount': 3000},
        }]
        
        context = BrowserContext(
            browser = Browser(config = BrowserConfig(headless=True)),
            config = BrowserContextConfig(
                save_recording_path ='recordings',
                browser_window_size = {'width': 1280, 'height': 500},
            )
        )

        self.browserContext = context

        self.firts_agent_history = []
        self.second_agent_history = []


    async def run_firts_agent(self, prompt: str) :
        controller = Controller()

        @controller.action('If a pop up appears, close it')
        async def close_pop_up(browser: Browser):
            page = await browser.get_current_page()

            close_button = await page.query_selector('.close-button')




        agent = Agent(
            task="""Click on the search icon that is on the top right corner of the page. If a pop-up appears, use the custom function close_pop_up.
            """,
            llm=ChatOpenAI(model='gpt-4o'),
            browser_context=self.browserContext,
            initial_actions=self.initial_actions,
            controller=Controller(),
        )

        await agent.run()

        # firstAgentController=Controller(output_model=ButtonsNamesOutput)

        # firts_agent = Agent(
        #     task=prompt,
        #     llm=ChatOpenAI(model='gpt-4o'),
        #     browser_context=self.browserContext,
        #     initial_actions=self.initial_actions,
        #     controller=firstAgentController,
        # )

        # self.firts_agent_history = await firts_agent.run()

        # result = self.firts_agent_history.final_result()

        # if result:
        #     buttons: ButtonsNamesOutput = ButtonsNamesOutput.model_validate_json(result)

        #     for button_name in buttons:
        #         print(f'Button Name: {button_name}')

        #         return buttons
        # else:
        #     raise Exception('No buttons found')
        

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
            
            return buttons
        else:
            raise Exception('No buttons found')
        

    async def check(self) -> ButtonCheckerAgentOutputs:
        await self.run_firts_agent(prompt=STEP)

        # print(f'Buttons found: {buttons_names}')

        # prompt = STEP_2 + '\n'.join([f"- {button_name}" for button_name in buttons_names])

        # buttons_output = await self.run_second_agent(prompt=prompt)

        # print(f'Buttons output: {buttons_output.outputs}')

        await self.browserContext.close()

        # return buttons_names
        

        


