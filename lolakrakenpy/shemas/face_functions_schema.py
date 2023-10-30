from pydantic import BaseModel

class FaceCropSchema(BaseModel):
    tracerId: str | None
    session: object | None
    image: object | None
    image_b64: str | None
    image_url: str | None
    enableEncodings: bool | None

class FaceMatchSchema(BaseModel):
    tracerId: str | None
    session: object | None
    image1: object | None
    image1_b64: str | None
    image1_url: str | None
    image2: object | None
    image2_b64: str | None
    image2_url: str | None
    enableEncodings: bool | None