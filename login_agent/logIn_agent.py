from abc import ABC, abstractmethod
import os
from utils.load_json_file import load_json_file
from utils.save_json_file import save_json_file
from browser_use import Agent, BrowserConfig, Browser, Controller, ActionResult
from pydantic import SecretStr
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_google_genai import ChatGoogleGenerativeAI
from .logIn_agent_output import LogInAgentOutput

class LogInAgent():
    def __init__(
            self,
            initialActions: list,
            emailLogInTaskPrompt:str,
            telephoneOperatorTaskPrompt:str,
            agentPath: str,
            api_key: str,
            messageContext: str = None,
        ):

        self.initialActions= initialActions

        self.emailLogInTaskPrompt = emailLogInTaskPrompt
        self.telephoneOperatorTaskPrompt = telephoneOperatorTaskPrompt
    
        self.agentPath = agentPath

        self.browser = Browser(config = BrowserConfig(headless=True)) 

        context = BrowserContext(
            browser = self.browser,
            config = BrowserContextConfig()
        )

        self.browserContext = context

        self.api_key = api_key

        self.messageContext = messageContext

    async def runEmailLogIn(self, email: str, password: str) -> LogInAgentOutput:
        controller = Controller(output_model=LogInAgentOutput, exclude_actions=['search_google', 'go_to_url'])

        prompt = self.emailLogInTaskPrompt

        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initialActions,
            controller=controller,
            sensitive_data={'email_value': email, 'password_value': password},
        )

        emailLogInHistory = await agent.run()

        emailLogInHistory.save_to_file(self.agentPath + '/emailLogInHistory.json')
        result = emailLogInHistory.final_result()
        save_json_file(self.agentPath, 'emailLogInResult', result)

        await self.browser.close()
        await self.browserContext.close()

        if result:
            logInOutput: LogInAgentOutput = LogInAgentOutput.model_validate_json(result)
            return logInOutput
        else:
            raise Exception('No result returned from LogInAgent')

    async def runTelephoneOperatorLogIn(self, operatorName: str, telephoneCode: str, telephoneNumber: str) -> LogInAgentOutput:
        controller = Controller(output_model=LogInAgentOutput)

        prompt = (self.telephoneOperatorTaskPrompt.
                replace('operator_name', operatorName).
                replace('telephone_code', telephoneCode).
                replace('telephone_number', telephoneNumber).
                replace('username', f"58{telephoneCode.replace('0', '')}{telephoneNumber}")
            )

        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(self.api_key)),
            browser_context=self.browserContext,
            initial_actions=self.initialActions,
            controller=controller,
        )

        telephoneOperatorLogInHistory = await agent.run()

        telephoneOperatorLogInHistory.save_to_file(self.agentPath + '/telephoneOperatorLogInHistory.json')
        result = telephoneOperatorLogInHistory.final_result()
        save_json_file(self.agentPath, 'telephoneOperatorLogInResult', result)

        await self.browser.close()
        await self.browserContext.close()

        if result:
            logInOutput: LogInAgentOutput = LogInAgentOutput.model_validate_json(result)
            return logInOutput
        else:
            raise Exception('No result returned from LogInAgent')