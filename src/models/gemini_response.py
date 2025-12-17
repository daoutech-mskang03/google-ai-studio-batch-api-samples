from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from zoneinfo import ZoneInfo

from src.models.gemini_common import Content
from src.models.gemini_request import RequestBody


def convert_utc_to_kst(v) -> Optional[datetime]:
    """UTC datetime 문자열을 KST datetime으로 변환"""
    if v is None:
        return None
    if isinstance(v, str):
        dt_utc = datetime.fromisoformat(v.replace('Z', '+00:00'))
        return dt_utc.astimezone(ZoneInfo('Asia/Seoul'))
    return v


class TokensDetail(BaseModel):
    """토큰 상세 모델"""
    modality: str = Field(..., description="모달리티 유형 (예: TEXT, IMAGE 등)")
    tokenCount: int = Field(..., description="토큰 수")


class UsageMetadata(BaseModel):
    """사용량 메타데이터 모델"""
    candidatesTokenCount: Optional[int] = Field(default=None, description="후보 토큰 수")
    candidatesTokensDetails: Optional[List[TokensDetail]] = Field(default=None, description="후보 토큰 상세")
    promptTokenCount: Optional[int] = Field(default=None, description="프롬프트 토큰 수")
    promptTokensDetails: Optional[List[TokensDetail]] = Field(default=None, description="프롬프트 토큰 상세")
    totalTokenCount: Optional[int] = Field(default=None, description="총 토큰 수")
    trafficType: Optional[str] = Field(default=None, description="트래픽 유형")


class Candidate(BaseModel):
    """후보 모델"""
    avgLogprobs: float = Field(..., description="평균 로그 확률")
    content: Content = Field(..., description="콘텐츠")
    finishReason: str = Field(..., description="완료 이유")


class ResponseBody(BaseModel):
    """응답 본문 모델"""
    candidates: List[Candidate] = Field(default_factory=list)
    createTime: Optional[datetime] = Field(default=None, description="응답 생성 시간")
    modelVersion: Optional[str] = Field(default=None, description="사용된 모델 버전")
    responseId: Optional[str] = Field(default=None, description="응답 ID")
    usageMetadata: Optional[UsageMetadata] = Field(default=None, description="사용량 메타데이터")

    @field_validator('createTime', mode='before')
    def convert_createtime_to_kst(cls, v):
        return convert_utc_to_kst(v)


class GeminiResponse(BaseModel):
    """Gemini API 응답 모델"""
    status: str = Field(..., description="응답 상태(성공: 빈 문자열, 실패: 오류 메시지)")
    processed_time: datetime = Field(..., description="처리 시간")
    request: RequestBody = Field(..., description="요청 본문")
    response: ResponseBody = Field(default_factory=ResponseBody, description="응답 본문(실패 시 빈 객체)")

    @field_validator('processed_time', mode='before')
    def convert_processed_time_to_kst(cls, v):
        return convert_utc_to_kst(v)

    def __str__(self):
        return f"<GeminiResponse status={self.status} processed_time={self.processed_time} response={self.response}>"