
from pydantic import BaseModel

class OcrGenericSchema(BaseModel):
    url: str = None
    imgBase64: str = None