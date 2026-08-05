"""Presigned OSS 直传契约。"""

import base64
import binascii

from pydantic import Field, field_validator, model_validator

from web.schemas import BaseSchema

# 本模块方法
from .file_info import FileInfoOut


class PresignFileRequest(BaseSchema):
    file_id: str = Field(pattern=r"^[0-9a-fA-F]{32}$")
    file_name: str = Field(min_length=1, max_length=255)
    file_size: int = Field(ge=0)
    content_type: str = Field(min_length=1, max_length=255)

    @field_validator("file_id")
    @classmethod
    def normalize_file_id(cls, value: str) -> str:
        return value.lower()


class PresignUploadRequest(PresignFileRequest):
    content_md5: str

    @field_validator("content_md5")
    @classmethod
    def validate_content_md5(cls, value: str) -> str:
        try:
            decoded = base64.b64decode(value, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("content_md5 必须是 Base64 编码") from exc
        if len(decoded) != 16:
            raise ValueError("content_md5 必须表示 16 字节 MD5")
        return value

    @model_validator(mode="after")
    def validate_digest_matches_file_id(self):
        decoded = base64.b64decode(self.content_md5, validate=True)
        if decoded.hex() != self.file_id:
            raise ValueError("content_md5 与 file_id 不一致")
        return self


class PresignCompleteRequest(PresignFileRequest):
    pass


class PresignUploadOut(BaseSchema):
    skip_upload: bool
    presigned_url: str | None = None
    expires_in: int
    file_id: str
    data: FileInfoOut | None = None


class PresignDownloadOut(BaseSchema):
    url: str
    expires_in: int
