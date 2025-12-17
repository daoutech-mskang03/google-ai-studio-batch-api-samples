# google-ai-studio-batch-api-samples
> [개발센터 세미나] Google AI Studio에서의 Batch API 샘플 코드

### 프로젝트 구조
```
google-ai-studio-batch-api-samples/
├── data/
│   └── batch_requests/                             # 배치 요청 데이터 저장 디렉토리
├── src/                                            # 소스 코드 메인 디렉토리
│   ├── models/
│   │   ├── gemini_common.py                        # Gemini API 요청/응답 공통 모델 정의
│   │   ├── gemini_request.py                       # Gemini API 요청 모델 정의
│   │   └── gemini_response.py                      # Gemini API 응답 모델 정의
│   └── utils/
│       ├── jsonl.py                                # JSONL 파일 처리 유틸리티
│       └── sample.py                               # 샘플 스크립트
├── README.md                                       # 프로젝트 설명 문서
└── requirements.txt                                # Python 패키지 의존성 목록
```

### 실행 환경 세팅 방법(MacOS)
1. 가상 환경 생성 및 활성화
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
2. pip 업그레이드
   ```bash
   pip install --upgrade pip
   ```
   
3. 의존성 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```