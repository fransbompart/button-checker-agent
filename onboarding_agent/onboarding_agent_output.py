from pydantic import BaseModel

class OnboardingAgentOutput(BaseModel):
    questionsAsked: list[str]
    answersGived: list[str]
    modelMessage: str
    successOnboarding: bool