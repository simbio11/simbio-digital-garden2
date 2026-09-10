import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

vault_path = Path(r"C:\Simbio")
quartz_content_path = Path(r"C:\Users\cmksc\quartz\content")
quartz_repo_path = Path(r"C:\Users\cmksc\quartz")

# 볼트 소스 경로가 쿼츠 폴더명과 다른 경우의 매핑.
# (2026-09-09 볼트 개편으로 00. 봇 운영 시스템/보고서 → _헤르메스/보고서 로 이동)
FOLDER_MAPPINGS = {
    "보고서": vault_path / "_헤르메스" / "보고서",
    "5. 독서, 노트": vault_path / "5. 독서, 노트",
}

# 사이트에 올리지 않을 볼트 상대경로(posix). quartz.config.yaml 의 ignorePatterns 와 일치시킬 것.
EXCLUDE_REL_PREFIXES = (
    "5. 독서, 노트/생각",
    # 케이스리포트(환자 식별정보 포함) — 2026-09-10 볼트에서 6. 개발,자산/임상례 로 이동(비공개).
    "7. 첨부·자료/임상례",
)

# 개별 파일 단위 비공개 목록(content/ 기준 상대경로). scripts/phi_exclude.txt 참조.
PHI_EXCLUDE_FILE = quartz_repo_path / "scripts" / "phi_exclude.txt"


def _load_phi_excludes():
    if not PHI_EXCLUDE_FILE.exists():
        return set()
    items = set()
    for line in PHI_EXCLUDE_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            items.add(line)
    return items


PHI_EXCLUDES = _load_phi_excludes()


def is_excluded(rel_path: Path) -> bool:
    rel = rel_path.as_posix()
    if rel in PHI_EXCLUDES:
        return True
    return any(rel == p or rel.startswith(p + "/") for p in EXCLUDE_REL_PREFIXES)


def sync_folders():
    print(f"[{datetime.now()}] Starting Obsidian to Quartz sync...")
    if not quartz_content_path.exists():
        print(f"Error: Quartz content path {quartz_content_path} does not exist.")
        return False

    # 동기화 대상 = 이미 content/ 에 있는 폴더 ∪ 명시 매핑된 폴더(없으면 새로 만든다)
    targets = {
        item.name
        for item in quartz_content_path.iterdir()
        if item.is_dir() and not item.name.startswith(".")
    }
    targets |= set(FOLDER_MAPPINGS.keys())

    updated_count = 0
    missing_sources = []

    for folder_name in sorted(targets):
        src_folder = FOLDER_MAPPINGS.get(folder_name, vault_path / folder_name)
        dst_folder = quartz_content_path / folder_name

        if not src_folder.exists():
            # 조용히 넘어가면 사이트가 조용히 '동결'된다 → 반드시 경고를 남긴다.
            print(f"[WARN] Source folder not found in vault: {src_folder}  (folder '{folder_name}' skipped!)")
            missing_sources.append(folder_name)
            continue

        dst_folder.mkdir(parents=True, exist_ok=True)
        print(f"Syncing folder: {folder_name}")

        for src_root, dirs, files in os.walk(src_folder):
            # Prune hidden/system directories instead of only skipping their files
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
            rel_path = Path(os.path.relpath(src_root, src_folder))

            if rel_path.as_posix() == ".":
                rel_path = Path()
            if any(p.startswith('.') or p.startswith('_') for p in rel_path.parts):
                continue
            if rel_path != Path() and is_excluded(Path(folder_name) / rel_path):
                continue

            dst_root = dst_folder / rel_path if rel_path != Path() else dst_folder
            dst_root.mkdir(parents=True, exist_ok=True)

            for file in files:
                if file.startswith('.') or file.startswith('_'):
                    continue
                if is_excluded(Path(folder_name) / rel_path / file):
                    continue
                src_file = Path(src_root) / file
                dst_file = dst_root / file

                if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
                    shutil.copy2(src_file, dst_file)
                    print(f"Updated: {folder_name}/{file}")
                    updated_count += 1

    if missing_sources:
        print(f"[WARN] 매핑이 끊긴 폴더: {missing_sources} — 볼트 경로가 바뀌었는지 확인하세요.")

    print(f"Sync completed. Total files updated/added: {updated_count}")
    return updated_count > 0


def git_commit_and_push():
    os.chdir(quartz_repo_path)
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("No changes to commit in Quartz repo.")
        return

    print("Staging changes...")
    subprocess.run(["git", "add", "content/"], check=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"Auto-update obsidian notes: {timestamp}"
    print(f"Committing with message: '{commit_msg}'")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("Pushing to GitHub...")
    push_res = subprocess.run(["git", "push", "origin", "v5"], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("Successfully pushed to GitHub!")
    else:
        print(f"Git push failed: {push_res.stderr}")


def regen_home():
    """홈(index.md)의 현황도·저장소 카드 수·최근 생성 노트 목록을 다시 생성."""
    script = quartz_repo_path / "scripts" / "gen_home.mjs"
    if not script.exists():
        return
    try:
        subprocess.run(["node", str(script)], cwd=quartz_repo_path, check=True)
    except Exception as e:
        print(f"gen_home.mjs 실행 실패(무시하고 계속): {e}")


if __name__ == "__main__":
    sync_folders()
    # 볼트 변경 여부와 무관하게 홈 통계 최신화. git_commit_and_push 가 실제 변경분만 커밋한다.
    regen_home()
    git_commit_and_push()
