import json

from pydantic import BaseModel
from typing import List, Callable, Any


def to_jsonl_bytes(
        items: List[Any],
        serializer: Callable[[Any], str] = None
) -> bytes:
    """객체 리스트를 JSONL bytes로 변환"""
    if serializer:
        lines = [serializer(item) for item in items]
    else:
        # 기본: Pydantic BaseModel이면 model_dump_json, 아니면 json.dumps
        lines = []
        for item in items:
            if isinstance(item, BaseModel):
                lines.append(item.model_dump_json(exclude_none=True, by_alias=True))
            elif isinstance(item, dict):
                lines.append(json.dumps(item, ensure_ascii=False))
            else:
                raise ValueError(f"Unsupported type: {type(item)}")

    jsonl_string = "\n".join(lines)
    return jsonl_string.encode('utf-8')