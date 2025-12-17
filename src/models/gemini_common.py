from pydantic import BaseModel, Field
from typing import List, Union


class FileData(BaseModel):
    """파일 데이터 정보"""
    fileUri: str = Field(..., description="GCS 파일 URI")
    mimeType: str = Field(..., description="파일 MIME 타입")


class TextPart(BaseModel):
    """텍스트 파트"""
    text: str


class FileDataPart(BaseModel):
    """파일 데이터 파트"""
    fileData: FileData


# Union 타입으로 여러 파트 타입 지원
Part = Union[TextPart, FileDataPart]


class Content(BaseModel):
    """콘텐츠 모델"""
    role: str = Field(..., description="사용자 역할 (user, model 등)")
    parts: List[Part] = Field(..., description="콘텐츠 파트 리스트")
