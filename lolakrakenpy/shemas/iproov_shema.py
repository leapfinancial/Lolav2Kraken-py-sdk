
from pydantic import BaseModel

class metadataSchema(BaseModel):
    returnURL: str | None
    operation: str | None
    assuranceType: str | None
    lolaURL: str | None
    theme: object | None

class claimTokenSchema(BaseModel):
    baseUrl: str | None
    chatLead: object | None
    sessionStore: object  | None
    metadata: metadataSchema | None

class claimTokenSchemaCallback(BaseModel):
    baseUrl: str | None
    chatLead: object | None
    sessionStore: object  | None
    metadata: metadataSchema | None