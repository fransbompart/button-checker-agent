from pydantic import BaseModel

class EmailLogInMethod(BaseModel):
    email: str
    password: str

class TelephoneOperatorLogInMethod(BaseModel):
    operatorName: str
    telephoneCode: str
    telephoneNumber: str