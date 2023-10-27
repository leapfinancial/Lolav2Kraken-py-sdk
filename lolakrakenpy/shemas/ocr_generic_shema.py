
from pydantic import BaseModel

class OcrGeneric(BaseModel):
    url: str = None
    imgBase64: str = None