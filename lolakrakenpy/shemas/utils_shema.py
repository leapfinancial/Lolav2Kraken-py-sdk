
from pydantic import BaseModel


class claimTokenUrlSchema(BaseModel):
    baseUrl: str | None
    chatLead: object | None
    sessionStore: object | None
    metadata: object | None
    extraData : object | None
    
class claimTokenSchema(BaseModel):
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

