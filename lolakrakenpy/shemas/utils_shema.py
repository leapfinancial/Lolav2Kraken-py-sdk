
from typing import Optional
from pydantic import BaseModel


class claimTokenUrlSchema(BaseModel):
    baseUrl: Optional[str]
    chatLead: object | None
    sessionStore: object | None
    metadata: object | None
    extradata : object | None
    
class claimTokenSchema(BaseModel):
    chatLead: object | None
    sessionStore: object | None
    metadata: object | None
    extraData : Optional[object] = None


class validateAddressSchema(BaseModel):
    baseUrl: Optional[str]
    chatLead: object | None
    sessionStore: object | None
    metadata: object | None


class SendNotificationSchema(BaseModel):
    label: Optional[str]
    payload: object | None

class RequestExtradataParams(BaseModel): 
    token: str

