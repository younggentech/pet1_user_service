from enum import Enum
import uuid
from pydantic import BaseModel, Field


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class BaseRequest(BaseModel):
    request_id: uuid.UUID = Field(default_factory=uuid.uuid4())


class CreateUserRequest(BaseRequest):
    email: str
    first_name: str
    last_name: str
    gender: Gender
    password: str


class VerifyUserRequest(BaseRequest):
    user_id: uuid.UUID
    verification_code: int


class DeleteUserRequest(BaseRequest):
    user_id: uuid.UUID


class GetUserRequest(BaseRequest):
    user_id: uuid.UUID


class Status(Enum):
    OK = "ok"
    FAIL = "fail"
    VERIFICATE = "verificate"


class BaseResponse(BaseModel):
    status: Status
    msg: str
    response_id: uuid.UUID = Field(default_factory=uuid.uuid4())


class CreateUserResponse(BaseResponse):
    user_id: uuid.UUID


class VerifyUserResponse(BaseResponse):
    token: dict
