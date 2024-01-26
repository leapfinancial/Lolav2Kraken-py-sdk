
from pydantic import BaseModel


class claimTokenSchema(BaseModel):
    baseUrl: str | None
    chatLead: object | None
    sessionStore: object | None
    metadata: object | None


class validateAddressSchema(BaseModel):
    baseUrl: str | None
    chatLead: object | None
    sessionStore: object | None
    metadata: object | None


class SendNotificationSchema(BaseModel):
    label: str | None
    payload: object | None

class RequestExtradataParams(BaseModel): 
    token: str

