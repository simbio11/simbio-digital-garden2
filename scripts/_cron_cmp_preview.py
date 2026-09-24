# -*- coding: utf-8 -*-
"""미장 프리뷰 볼트 vs 미러 실제 내용 비교(변환 적용 후 바이트 비교) + mtime."""
import importlib.util
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

REPO = Path(r"C:\Users\cmksc\quartz")
spec = importlib.util.spec_from_file_location("syncmod", REPO / "sync_obsidian.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rel = Path("보고서/주식 브리핑/2026-09/W4/미장 프리뷰-2026-09-21.md")
src = mod.FOLDER_MAPPINGS["보고서"] / Path(*rel.parts[1:]) if rel.parts[0] == "보고서" else None
dst = mod.quartz_content_path / rel
print("vault:", src)
print("mirror:", dst)
for label, p in (("vault", src), ("mirror", dst)):
    st = p.stat()
    print(f"  {label}: {st.st_size}B · mtime {datetime.fromtimestamp(st.st_mtime):%Y-%m-%d %H:%M:%S}")

tmpd = Path(tempfile.mkdtemp(prefix="cmp_"))
t = tmpd / "x.md"
shutil.copy2(src, t)
raw = src.read_bytes()
try:
    mod.convert_custom_frames([t])
except Exception as e:
    print("convert 실패:", e)
    t.write_bytes(raw)
same = t.read_bytes() == dst.read_bytes()
print("변환본 == 미러 :", same)
if not same:
    a = t.read_text(encoding="utf-8", errors="replace").splitlines()
    b = dst.read_text(encoding="utf-8", errors="replace").splitlines()
    print(f"  줄수 vault {len(a)} / mirror {len(b)}")
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y][:10]
    for i in diff:
        print(f"  L{i+1}\n    vault : {a[i][:110]}\n    mirror: {b[i][:110]}")
shutil.rmtree(tmpd, ignore_errors=True)
