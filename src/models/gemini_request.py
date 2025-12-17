from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from src.models.gemini_common import FileData, TextPart, FileDataPart, Content


class ThinkingConfig(BaseModel):
    """사고 설정"""
    thinkingBudget: Optional[int] = Field(default=0, ge=0, description="사고 예산 (밀리초 단위)")


class GenerationConfig(BaseModel):
    """생성 설정"""
    temperature: Optional[float] = Field(default=None, ge=0, le=2, description="생성 온도")
    topP: Optional[float] = Field(default=None, ge=0, le=1, description="Top-p 샘플링")
    maxOutputTokens: Optional[int] = Field(default=None, gt=0, description="최대 출력 토큰 수")
    topK: Optional[int] = Field(default=None, gt=0, description="Top-k 샘플링")
    candidateCount: Optional[int] = Field(default=None, gt=0, description="생성할 후보 수")
    thinkingConfig: Optional[ThinkingConfig] = Field(default=None, description="사고 설정")


class RequestBody(BaseModel):
    """요청 본문"""
    systemInstruction: Optional[Content] = Field(default=None, description="시스템 지침")
    contents: List[Content] = Field(..., description="콘텐츠 리스트")
    generationConfig: Optional[GenerationConfig] = Field(default=None, description="생성 설정")
    labels: Optional[Dict[str, str]] = Field(default=None, description="요청 식별용 레이블 (키-값 쌍)")


class GeminiRequest(BaseModel):
    """Gemini API 요청 전체 모델"""
    request: RequestBody


# 사용 예시
if __name__ == "__main__":
    # 예제 데이터로 모델 생성
    example_request_1 = GeminiRequest(
        request=RequestBody(
            contents=[
                Content(
                    role="user",
                    parts=[
                        TextPart(text="What is the relation between the following video and image samples?"),
                        FileDataPart(
                            fileData=FileData(
                                fileUri="gs://cloud-samples-data/generative-ai/video/animals.mp4",
                                mimeType="video/mp4"
                            )
                        ),
                        FileDataPart(
                            fileData=FileData(
                                fileUri="gs://cloud-samples-data/generative-ai/image/cricket.jpeg",
                                mimeType="image/jpeg"
                            )
                        )
                    ]
                )
            ],
            generationConfig=GenerationConfig(
                temperature=0.9,
                topP=1.0,
                maxOutputTokens=256
            )
        )
    )

    example_request_2 = GeminiRequest(
        request=RequestBody(
            contents=[
                Content(
                    role="user",
                    parts=[
                        TextPart(text="Describe this image"),
                        FileDataPart(
                            fileData=FileData(
                                fileUri="gs://cloud-samples-data/generative-ai/image/car.jpeg",
                                mimeType="image/jpeg"
                            )
                        )
                    ]
                )
            ],
            generationConfig=GenerationConfig(
                temperature=0.5,
                maxOutputTokens=512
            )
        )
    )

    # JSONL 파일로 저장
    requests = [example_request_1, example_request_2]

    with open("gemini_requests.jsonl", "w", encoding="utf-8") as f:
        for req in requests:
            # 각 요청을 한 줄로 저장 (indent 없이)
            json_line = req.model_dump_json(exclude_none=True)
            f.write(json_line + "\n")

    print("✅ JSONL 파일 생성 완료: gemini_requests.jsonl")

    # JSONL 파일 읽기 예시
    print("\n📖 JSONL 파일 읽기:")
    with open("gemini_requests.jsonl", "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            # 각 줄을 파싱
            request = GeminiRequest.model_validate_json(line)
            print(
                f"Request {i}: {request.request.contents[0].parts[0].text if isinstance(request.request.contents[0].parts[0], TextPart) else 'N/A'}")