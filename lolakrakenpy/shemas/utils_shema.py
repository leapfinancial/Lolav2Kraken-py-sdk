
from pydantic import BaseModel

class claimTokenSchema(BaseModel):
    baseUrl: str | None
    chatLead: object | None
    sessionStore: object  | None
    metadata: object | None