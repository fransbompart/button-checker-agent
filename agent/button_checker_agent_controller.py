from browser_use import Controller, ActionResult, Browser
from .button_checker_agent_output import ButtonCheckerAgentOutputs

secondAgentController=Controller(output_model=ButtonCheckerAgentOutputs)

@secondAgentController.action('If clicking an element navigates to a new page, return to the previous one')
async def return_to_previous_page(browser: Browser):
    browser.back()
    return ActionResult(extracted_content='Returned to the original previous page')