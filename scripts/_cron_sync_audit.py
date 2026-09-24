# -*- coding: utf-8 -*-
"""무인 크론용: 볼트(C:\\Simbio) ↔ Quartz 미러(content/) 전수 대조.

sync_obsidian.py 의 복사 규칙(숨김/_ 접두 제외, EXCLUDE_REL_PREFIXES, phi_exclude.txt)을
그대로 재현해 3항목을 0으로 만드는 것이 목표:
  stale   : 미러에만 있음(유령 사본)
  newer   : 볼트가 미러보다 최신(동기화 누락)
  missing : 볼트에만 있음(복사 안 됨)
사용: python scripts/_cron_sync_audit.py [--list N]
"""
import os
import sys
from pathlib import Path

vault = Path(r"C:\Simbio")
content = Path(r"C:\Users\cmksc\quartz\content")
repo = Path(r"C:\Users\cmksc\quartz")

FOLDER_MAPPINGS = {
    "보고서": vault / "_헤르메스" / "보고서",
    "5. 독서, 노트": vault / "5. 독서, 노트",
}
EXCLUDE_REL_PREFIXES = ("5. 독서, 노트/생각", "7. 첨부·자료/임상례")

PHI = set()
_pf = repo / "scripts" / "phi_exclude.txt"
if _pf.exists():
    for _line in _pf.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#"):
            PHI.add(_line)


def hidden(name: str) -> bool:
    return name.startswith(".") or name.startswith("_")


def is_excluded(rel: Path) -> bool:
    r = rel.as_posix()
    if r in PHI:
        return True
    return any(r == p or r.startswith(p + "/") for p in EXCLUDE_REL_PREFIXES)


def vault_files(folder: str, src_folder: Path):
    out = set()
    for root, dirs, files in os.walk(src_folder):
        dirs[:] = [d for d in dirs if not hidden(d)]
        rel = Path(os.path.relpath(root, src_folder))
        if rel.as_posix() == ".":
            rel = Path()
        if any(hidden(p) for p in rel.parts):
            continue
        if rel != Path() and is_excluded(Path(folder) / rel):
            continue
        for f in files:
            if hidden(f):
                continue
            if is_excluded(Path(folder) / rel / f):
                continue
            out.add((rel / f) if rel != Path() else Path(f))
    return out


def mirror_files(dst_folder: Path):
    out = set()
    for p in dst_folder.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(dst_folder)
        if any(part.startswith(".") for part in rel.parts):
            continue
        out.add(rel)
    return out


def main():
    n_list = 40
    if "--list" in sys.argv:
        try:
            n_list = int(sys.argv[sys.argv.index("--list") + 1])
        except Exception:
            pass

    targets = sorted(
        item.name for item in content.iterdir() if item.is_dir() and not item.name.startswith(".")
    )
    stale, newer, missing, no_src = [], [], [], []
    v_total = m_total = 0

    for folder in targets:
        src_folder = FOLDER_MAPPINGS.get(folder, vault / folder)
        dst_folder = content / folder
        if not src_folder.exists():
            no_src.append(folder)
            continue
        vset = vault_files(folder, src_folder)
        mset = mirror_files(dst_folder)
        v_total += len(vset)
        m_total += len(mset)
        for rel in sorted(mset - vset):
            if rel.name == "index.md":
                continue  # 생성/관리 파일
            stale.append(f"{folder}/{rel.as_posix()}")
        for rel in sorted(mset & vset):
            sp = src_folder / rel
            mp = dst_folder / rel
            try:
                if sp.stat().st_mtime > mp.stat().st_mtime + 0.5:
                    newer.append(f"{folder}/{rel.as_posix()}")
            except OSError:
                pass
        for rel in sorted(vset - mset):
            missing.append(f"{folder}/{rel.as_posix()}")

    print(f"대상 폴더 {len(targets)}개 · 볼트 소스 파일 {v_total} · 미러 파일 {m_total}")
    if no_src:
        print(f"[WARN] 볼트 소스 없음: {no_src}")
    print(f"STALE(미러에만)  : {len(stale)}")
    print(f"NEWER(볼트가 최신): {len(newer)}")
    print(f"MISSING(미러 없음): {len(missing)}")
    for label, lst in (("STALE", stale), ("NEWER", newer), ("MISSING", missing)):
        for item in lst[:n_list]:
            print(f"   · [{label}] {item}")
        if len(lst) > n_list:
            print(f"   · [{label}] …외 {len(lst) - n_list}건")


if __name__ == "__main__":
    main()
