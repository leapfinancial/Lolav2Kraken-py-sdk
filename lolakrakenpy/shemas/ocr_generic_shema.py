
from pydantic import BaseModel

class OcrGeneric(BaseModel):
    url: str | None = None
    imgBase64: str | None = None