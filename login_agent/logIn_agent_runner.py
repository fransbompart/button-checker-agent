import os
from .logIn_agent import LogInAgent
from .logIn_agent_output import LogInAgentOutput
from .logIn_methods import EmailLogInMethod, TelephoneOperatorLogInMethod

from .soyZen.prompts import SOY_ZEN_EMAIL_LOGIN_TASK_PROMPT, SOY_ZEN_OPERATOR_LOGIN_TASK_PROMPT

from .tribuDeportiva.prompts import TRIBU_DEPORTIVA_EMAIL_LOGIN_TASK_PROMPT, TRIBU_DEPORTIVA_OPERATOR_LOGIN_TASK_PROMPT

class LogInAgentRunner: 
    @staticmethod
    async def run(logInMethod: EmailLogInMethod | TelephoneOperatorLogInMethod) -> LogInAgentOutput:
        api_key = os.getenv('GEMINI_API_KEY', '')

        agent = LogInAgent(
            initialActions=[
                {'open_tab': {'url': 'https://tribudeportiva.com/auth/login'}},
            ],
            emailLogInTaskPrompt = TRIBU_DEPORTIVA_EMAIL_LOGIN_TASK_PROMPT,
            telephoneOperatorTaskPrompt = TRIBU_DEPORTIVA_OPERATOR_LOGIN_TASK_PROMPT,
            agentPath = 'login_agent/tribuDeportiva',
            api_key = api_key,
        )

        if isinstance(logInMethod, EmailLogInMethod):
            return await agent.runEmailLogIn(
                email = logInMethod.email,
                password = logInMethod.password,
            ) 
        else:
            return await agent.runTelephoneOperatorLogIn(
                operatorName = logInMethod.operatorName,
                telephoneCode = logInMethod.telephoneCode,
                telephoneNumber = logInMethod.telephoneNumber,
            )



