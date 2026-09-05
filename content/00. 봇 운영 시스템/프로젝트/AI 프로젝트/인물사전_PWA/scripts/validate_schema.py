# -*- coding: utf-8 -*-
"""person-dict.schema.json 검증 스크립트"""
import json
import re
import os
import sys

WS = os.path.dirname(os.path.abspath(__file__))
# 스키마 파일 위치 자동 탐색:
# 1) 스크립트와 같은 폴더(워크스페이스) 2) 프로젝트 루트의 docs/ (볼트 scripts/ 배치 시)
SCHEMA_PATH = os.path.join(WS, "person-dict.schema.json")
if not os.path.exists(SCHEMA_PATH):
    cand = os.path.normpath(os.path.join(WS, "..", "docs", "person-dict.schema.json"))
    if os.path.exists(cand):
        SCHEMA_PATH = cand
    else:
        print("ERROR: person-dict.schema.json not found next to script or in ../docs/")
        sys.exit(2)

def main():
    # 1. 스키마 파일이 유효한 JSON인지
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    print("schema JSON parse: OK")
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert "required" in schema and schema["required"] == ["id", "name", "createdAt", "updatedAt"]
    print("schema structure: OK (draft-07, required fields OK)")

    # 2. jsonschema 라이브러리 유무
    try:
        import jsonschema
        validator = jsonschema.Draft7Validator(schema)
        mode = "lib"
    except ImportError:
        mode = "manual"
        print("jsonschema lib: NOT installed -> manual fallback")

    def check(person):
        if mode == "lib":
            errs = list(validator.iter_errors(person))
            return (len(errs) == 0), [e.message for e in errs]
        # manual fallback
        if not person.get("name"):
            return False, ["name required"]
        if "level" in person and not (1 <= person["level"] <= 5):
            return False, ["level range 1..5"]
        if "emotion" in person and person["emotion"] not in ("good", "neutral", "hard"):
            return False, ["emotion enum"]
        if "metAt" in person and person["metAt"] and not re.match(r"^\d{4}-\d{2}-\d{2}$", person["metAt"]):
            return False, ["metAt pattern"]
        if "tags" in person and len(person["tags"]) != len(set(person["tags"])):
            return False, ["tags unique"]
        return True, []

    valid_samples = [
        {"id": "lxyz123", "name": "김비비", "place": "커피빈 강남점",
         "metAt": "2026-08-15", "emotion": "good", "level": 3,
         "tags": ["business", "school"], "memo": "🗣 자녀가 중3, 의대 지망",
         "createdAt": 1788250000000, "updatedAt": 1788250000000},
        {"id": "abc", "name": "최소 기록", "createdAt": 1, "updatedAt": 1},
        {"id": "max", "name": "가" * 50, "place": "가" * 100, "memo": "가" * 5000,
         "tags": ["business", "personal", "family", "school", "community"],
         "level": 5, "emotion": "hard", "metAt": "2026-01-01",
         "createdAt": 1, "updatedAt": 1},
    ]
    invalid_samples = [
        {"id": "x", "name": "", "createdAt": 1, "updatedAt": 1},
        {"id": "x", "name": "a", "level": 6, "createdAt": 1, "updatedAt": 1},
        {"id": "x", "name": "a", "emotion": "great", "createdAt": 1, "updatedAt": 1},
        {"id": "x", "name": "a", "tags": ["business", "business"], "createdAt": 1, "updatedAt": 1},
        {"id": "x", "name": "a", "metAt": "2026/08/15", "createdAt": 1, "updatedAt": 1},
        {"id": "x", "name": "a", "createdAt": 1, "updatedAt": 1, "unknown": "extra"},
        {"id": "x", "name": "a", "createdAt": 1},  # updatedAt 누락
    ]

    ok = True
    for i, p in enumerate(valid_samples):
        good, msgs = check(p)
        status = "PASS" if good else "FAIL: " + "; ".join(msgs)
        print(f"valid[{i}]: {status}")
        ok = ok and good
    for i, p in enumerate(invalid_samples):
        good, msgs = check(p)
        status = "correctly rejected" if not good else "!! UNEXPECTED PASS"
        print(f"invalid[{i}]: {status}")
        ok = ok and (not good)

    # 3. 프로토타입 app.js의 TAGS/EMOTIONS/LEVEL 상수와 스키마 enum 일치 확인
    app_js = r"C:/Simbio/00. 봇 운영 시스템/프로젝트/AI 프로젝트/인물사전_PWA/public/app.js"
    if os.path.exists(app_js):
        src = open(app_js, encoding="utf-8").read()
        tag_keys = re.findall(r"^\s{2}(business|personal|family|school|community):", src, re.M)
        emotion_keys = re.findall(r"^\s{2}(good|neutral|hard):", src, re.M)
        schema_tags = schema["properties"]["tags"]["items"]["enum"]
        schema_emotions = schema["properties"]["emotion"]["enum"]
        print("app.js tags:", sorted(set(tag_keys)), "== schema:", sorted(schema_tags), sorted(set(tag_keys)) == sorted(schema_tags))
        print("app.js emotions:", sorted(set(emotion_keys)), "== schema:", sorted(schema_emotions), sorted(set(emotion_keys)) == sorted(schema_emotions))
    else:
        print("app.js not found at expected path (skip cross-check)")

    print("RESULT:", "ALL PASS" if ok else "SOME FAILURES")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
