import os
from .onboarding_agent import OnboardingAgent
from .onboarding_agent_output import OnboardingAgentOutput

from .soyZen.prompts import SOY_ZEN_ONBOARDING_TASK_PROMPT, SOY_ZEN_ONBOARDING_SYSTEM_MESSAGE_PROMPT

class OnboardingAgentRunner:
    @staticmethod
    async def run(email: str, password: str) -> OnboardingAgentOutput:
        api_key = os.getenv('GEMINI_API_KEY', '')

        agent = OnboardingAgent(
            initialActions=[
                {'open_tab': {'url': 'https://soyzen.com/test-constructor'}},
            ],
            taskPrompt=SOY_ZEN_ONBOARDING_TASK_PROMPT,
            agentPath='onboarding_agent/soyZen',
            api_key=api_key,
            messageContext=SOY_ZEN_ONBOARDING_SYSTEM_MESSAGE_PROMPT,
        )

        return await agent.run(email = email, password = password)

