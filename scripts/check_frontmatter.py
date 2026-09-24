import sys, io
from pathlib import Path

try:
    import yaml
except ImportError:
    print("NO_PYYAML")
    sys.exit(2)

root = Path(r"C:\Users\cmksc\quartz\content")
bad = []
files = list(root.rglob("*.md"))
print("scanning %d md files" % len(files))
for p in files:
    try:
        text = p.read_text(encoding="utf-8")
    except Exception as e:
        bad.append((str(p), "READ_ERROR %s" % e))
        continue
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.lstrip().startswith("---"):
        continue
    lines = text.splitlines()
    # find opening fence
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if lines[idx].strip() != "---":
        continue
    end = None
    for j in range(idx + 1, len(lines)):
        if lines[j].strip() == "---":
            end = j
            break
    if end is None:
        continue
    fm = "\n".join(lines[idx + 1:end])
    try:
        yaml.safe_load(fm)
    except Exception as e:
        bad.append((str(p.relative_to(root)), str(e).splitlines()[0]))
        continue
    # 2026-09-19: 중복 매핑 키는 PyYAML 이 조용히 통과시키고 Quartz(js-yaml)만 fatal 로 죽인다.
    seen, dups = set(), []
    for ln in lines[idx + 1:end]:
        if not ln or ln[0] in " \t-":
            continue
        s = ln.strip()
        if ":" not in s or s.startswith("#"):
            continue
        key = s.split(":", 1)[0].strip()
        if key in seen and key not in dups:
            dups.append(key)
        seen.add(key)
    if dups:
        bad.append((str(p.relative_to(root)), "duplicated mapping key: " + ", ".join(dups)))

print("BAD FRONTMATTER: %d" % len(bad))
for f, e in bad:
    print(" - %s :: %s" % (f, e))
