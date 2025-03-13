import os
from utils.load_json_file import load_json_file
from utils.save_json_file import save_json_file
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_google_genai import ChatGoogleGenerativeAI
from .onboarding_agent_output import OnboardingAgentOutput

class OnboardingAgent:
    def __init__(
            self,
            initialActions: list,
            taskPrompt:str,
            agentPath: str,
            api_key: str,
            messageContext: str = None,
        ):

        self.initialActions= initialActions

        self.taskPrompt = taskPrompt

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

    async def run(self, email: str, password: str) -> OnboardingAgentOutput:
        controller = Controller(output_model=OnboardingAgentOutput)

        # prompt = self.taskPrompt
        prompt = f"## System Message\n{self.messageContext}\n---\n## Task\n{self.taskPrompt}"

        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initialActions,
            controller=controller,
            planner_llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
            message_context=self.messageContext,
            sensitive_data={'email_value': email, 'password_value': password},
        )

        onboardingHistory = await agent.run()

        onboardingHistory.save_to_file(self.agentPath + '/onboardingHistory.json')
        result = onboardingHistory.final_result()
        save_json_file(self.agentPath, 'onboardingResult', result)

        await self.browser.close()
        await self.browserContext.close()

        if result:
            onboardingOutput: OnboardingAgentOutput = OnboardingAgentOutput.model_validate_json(result)
            return onboardingOutput
        else: 
            raise Exception("OnboardingAgent did not return a result")