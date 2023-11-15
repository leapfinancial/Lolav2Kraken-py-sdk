
from pydantic import BaseModel

class claimTokenSchema(BaseModel):
    chatLead: object | None
    sessionStore: object  | None
    metadata: object | None