"""특정 basename 노트의 볼트/미러 현황을 정확히(UTF-8) 확인한다.

사용: python scripts/_cron_find_notes.py [이름1 이름2 ...]
"""
import sys
from pathlib import Path

VAULT = Path(r"C:\Simbio")
MIRROR = Path(r"C:\Users\cmksc\quartz\content")
NAMES = sys.argv[1:] or [
    "드퀘르벵 증후군", "경추 척수증", "심근경색증", "늑골 골절",
    "총경동맥", "베타차단제", "소경활혈탕", "대호경간탕",
]


def scan(root: Path, name: str):
    hits = []
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if p.stem == name:
            try:
                st = p.stat()
            except OSError:
                continue
            hits.append(f"{rel}  ({st.st_size}B, mtime={int(st.st_mtime)})")
    return hits


for n in NAMES:
    v, m = scan(VAULT, n), scan(MIRROR, n)
    print(f"\n### {n}")
    print("  VOLT :", "; ".join(v) if v else "없음")
    print("  MIRR:", "; ".join(m) if m else "없음")
