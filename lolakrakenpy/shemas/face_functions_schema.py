from pydantic import BaseModel

class FaceCropSchema(BaseModel):
    tracerId: str | None =None
    session: object | None =None
    image: object | None =None
    image_b64: str | None =None
    image_url: str | None =None
    enableEncodings: bool | None=None   

class FaceMatchSchema(BaseModel):
    tracerId: str | None =None
    session: object | None =None
    image1: object | None =None
    image1_b64: str | None =None
    image1_url: str | None =None
    image2: object | None =None
    image2_b64: str | None =None
    image2_url: str | None =None
    enableEncodings: bool | None =None