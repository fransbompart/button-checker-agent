from browser_use import Controller, Agent, Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext

from langchain_openai import ChatOpenAI

from .button_checker_agent_output import ButtonCheckerAgentOutputs

TASK = """

### Prompt for Page Buttons Checker Agent 

**Objective:**
In the current view of the page, identify all actionable elements (such as buttons, links, or interactive components) and systematically test if they function as expected. For each element:

- Click it and observe the resulting change on the page.
- Provide a brief description of what happened after the interaction.
- Determine if the observed result aligns with the expected behavior based on the element’s label or appearance.

**Important:**
- If clicking an element navigates to a new page, return to the original page before proceeding with the next element.
- Ensure all interactions are performed without missing any identified elements.
- Maintain a structured record of interactions, including the element name, observed result, and success status (true/false).

---

### Step 1: Identify Actionable Elements

- Scan the webpage and identify all clickable elements.
- Assign a meaningful name to each element based on what it represents (e.g., a profile icon should be labeled as "Profile Button").

---

### Step 2: Click Each Button and Analyze the Interaction

- Click on each identified button.
- Observe the result of the action and summarize it in a short description.
- Determine if the result aligns with the button's expected function:
 - If the action matches the button’s name, set result_success = True.
 - If the action does not match the button’s name, set result_success = False.
 - If the button leads to a new page, return to the previous page and continue checking the remaining buttons.
"""

class ButtonCheckerAgent():
    def __init__(self):

        self.initial_actions= [
            {
                'open_tab': {
                    'url': 'https://soyzen.com/home'
                }
            }
        ]
                
        # browser = Browser()
        # context = BrowserContext(
        #     browser=browser,
        #     config=BrowserContextConfig(
        #         save_recording_path='recordings',
        # ))

        # self.browser = browser
        # self.browserContext = context

        self.controller = Controller(
            output_model=ButtonCheckerAgentOutputs,
        )

        self.history = []

        self.agent = Agent(
            task=TASK,
            llm=ChatOpenAI(model='gpt-4o'),
            browser=Browser(),
            initial_actions=self.initial_actions,
        )

    async def check(self):
        await self.agent.run()

        input("Press Enter to close the browser...")

        await self.browser.close()

        

        


