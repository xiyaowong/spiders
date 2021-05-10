from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    ok: bool
    msg: str = ''
