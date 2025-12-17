import os
import io
import time

from google import genai
from google.genai import types

from src.models.gemini_request import GeminiRequest, RequestBody, GenerationConfig, ThinkingConfig
from src.models.gemini_common import Content, TextPart, FileDataPart, FileData
from src.utils.jsonl import to_jsonl_bytes


TEST_DATA = [
    ("/paths/to/your/image1.jpg", "이 이미지를 설명해줘."),
    ("/paths/to/your/image2.png", "이 로고에 해당하는 애플리케이션의 이름은 무엇인가요?"),
]


if __name__ == '__main__':
    client = genai.Client(
        api_key="GOOGLE-API-KEY-HERE"
    )

    print(f"#1. 파일 업로드")
    uploaded_datas = []
    for file_path, prompt in TEST_DATA:
        my_file = client.files.upload(file=file_path)
        uploaded_datas.append((my_file, prompt))
        print(f"  - 업로드된 파일: {my_file.name} (ID: {my_file.display_name}, MIME: {my_file.mime_type})")

    print(f"#2. jsonline 요청 생성 및 업로드")
    jsonlines = []
    for my_file, prompt in uploaded_datas:
        request = GeminiRequest(
            request=RequestBody(
                contents=[
                    Content(
                        role='user',
                        parts=[
                            FileDataPart(
                                fileData=FileData(
                                    fileUri=my_file.uri,
                                    mimeType=my_file.mime_type
                                )
                            ),
                            TextPart(text=prompt)
                        ]
                    )
                ],
                generationConfig=GenerationConfig(
                    maxOutputTokens=512,
                    thinkingConfig=ThinkingConfig(
                        thinkingBudget=0,
                    )
                )
            )
        )
        jsonlines.append(request)

    jsonl_bytes = to_jsonl_bytes(jsonlines)

    os.makedirs("../data/batch_requests", exist_ok=True)
    local_path = f"../data/batch_requests/{int(time.time())}_gemini_requests.jsonl"
    with open(local_path, "wb") as f:
        f.write(jsonl_bytes)
        print(f"  - 로컬에 JSONL 파일 저장: {local_path}")

    jsonl_file = client.files.upload(
        file=io.BytesIO(jsonl_bytes),
        config=types.UploadFileConfig(
            display_name="my_gemini_batch_request",
            mime_type='jsonl'
        )
    )
    print(f"  - 업로드된 JSONL 파일: {jsonl_file.name} (ID: {jsonl_file.display_name}, MIME: {jsonl_file.mime_type})")

    print(f"#3. Gemini 배치 작업 생성")
    batch_job = client.batches.create(
        model="gemini-2.5-flash-lite",
        src=jsonl_file.name,
    )
    print(f"  - 생성된 배치 작업: {batch_job.name}, 상태: {batch_job.state}")
    print(f"  - 요청 시각: {batch_job.create_time}")

    print(f"#4. 배치 작업 상태 확인")
    while True:
        time.sleep(10)  # 10초 대기
        job = client.batches.get(name=batch_job.name)
        print(f"  - 배치 작업 상태: {job.state}")

        if job.state in [types.JobState.JOB_STATE_SUCCEEDED, types.JobState.JOB_STATE_FAILED]:
            print("  - 배치 작업 완료됨.")
            break

    print(f"#5. 배치 작업 결과 가져오기")
    if job.dest and job.dest.file_name:
        result_file_name = job.dest.file_name
        print(f"  - 결과 파일 이름: {result_file_name}")

        print("file content 다운로드 중...")
        file_content = client.files.download(file=result_file_name)
        print(file_content.decode('utf-8'))
    elif job.dest and job.dest.inlined_responses:
        # Results are inline
        print("Results are inline:")
        for i, inline_response in enumerate(job.dest.inlined_responses):
            print(f"Response {i + 1}:")
            if inline_response.response:
                # Accessing response, structure may vary.
                try:
                    print(inline_response.response.text)
                except AttributeError:
                    print(inline_response.response)  # Fallback
            elif inline_response.error:
                print(f"Error: {inline_response.error}")
    else:
        print("No results found (neither file nor inline).")

