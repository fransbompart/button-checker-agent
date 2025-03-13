from pydantic import BaseModel

class LogInAgentOutput(BaseModel):
    successLogIn: bool
    modelMessage: str