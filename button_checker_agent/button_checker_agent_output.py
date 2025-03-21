from pydantic import BaseModel
from typing import List

class ButtonsNamesOutput(BaseModel):
    button_name: List[str]

class ButtonCheckerAgentOutput(BaseModel): 
    button_name: str
    button_action_result_description: str
    button_action_result_success: bool

class ButtonCheckerAgentOutputs(BaseModel):
    outputs: List[ButtonCheckerAgentOutput]


