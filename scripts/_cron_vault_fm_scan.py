"""볼트 전체 프런트매터 프리플라이트: YAML 파싱 오류 + 중복 최상위 키 탐지.

PyYAML safe_load 는 중복 키를 조용히 덮어쓰므로 줄 단위로도 최상위 키를 센다.
사용: python scripts/_cron_vault_fm_scan.py [볼트루트]
"""
import sys
from pathlib import Path

try:
    import yaml
except Exception as e:  # pragma: no cover
    print("PyYAML 없음:", e)
    sys.exit(2)

root = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Simbio")
bad_yaml = []
dup_keys = []
n = 0
for p in root.rglob("*.md"):
    if any(part.startswith((".", "_")) for part in p.relative_to(root).parts):
        continue
    n += 1
    try:
        raw = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    if not raw.startswith("---"):
        continue
    end = raw.find("\n---", 3)
    if end == -1:
        bad_yaml.append((str(p.relative_to(root)), "unterminated frontmatter"))
        continue
    block = raw[3:end]
    try:
        yaml.safe_load(block)
    except Exception as e:
        bad_yaml.append((str(p.relative_to(root)), str(e).splitlines()[0]))
    # 줄 단위 중복 최상위 키
    keys = [ln.split(":", 1)[0].strip() for ln in block.splitlines()
            if ln and not ln[0].isspace() and ":" in ln and not ln.lstrip().startswith("#")]
    seen, dups = set(), []
    for k in keys:
        if k in seen and k not in dups:
            dups.append(k)
        seen.add(k)
    if dups:
        dup_keys.append((str(p.relative_to(root)), dups))

print(f"스캔 {n}개 md · YAML오류 {len(bad_yaml)} · 중복키 {len(dup_keys)}")
for rel, msg in bad_yaml[:20]:
    print(f"  [YAML] {rel} -> {msg}")
for rel, dups in dup_keys[:20]:
    print(f"  [DUPKEY] {rel} -> {dups}")
