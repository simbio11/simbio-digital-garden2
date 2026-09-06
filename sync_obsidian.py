import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

vault_path = Path(r"C:\Simbio")
quartz_content_path = Path(r"C:\Users\cmksc\quartz\content")
quartz_repo_path = Path(r"C:\Users\cmksc\quartz")

# Content folder names whose vault source lives under a DIFFERENT path than the name.
# (vault has no top-level "보고서"; the canonical source is 00. 봇 운영 시스템/보고서)
FOLDER_MAPPINGS = {
    "보고서": vault_path / "00. 봇 운영 시스템" / "보고서",
}

def sync_folders():
    print(f"[{datetime.now()}] Starting Obsidian to Quartz sync...")
    if not quartz_content_path.exists():
        print(f"Error: Quartz content path {quartz_content_path} does not exist.")
        return False

    updated_count = 0

    for item in quartz_content_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            folder_name = item.name
            src_folder = FOLDER_MAPPINGS.get(folder_name, vault_path / folder_name)
            dst_folder = item

            if not src_folder.exists():
                print(f"Source folder not found in vault: {src_folder}")
                continue

            print(f"Syncing folder: {folder_name}")

            for src_root, dirs, files in os.walk(src_folder):
                # Prune hidden/system directories instead of only skipping their files
                dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
                rel_path = os.path.relpath(src_root, src_folder)
                if rel_path == '.':
                    dst_root = dst_folder
                else:
                    dst_root = dst_folder / rel_path

                if any(p.startswith('.') or p.startswith('_') for p in Path(rel_path).parts):
                    continue

                dst_root.mkdir(parents=True, exist_ok=True)

                for file in files:
                    if file.startswith('.') or file.startswith('_'):
                        continue
                    src_file = Path(src_root) / file
                    dst_file = dst_root / file

                    if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
                        shutil.copy2(src_file, dst_file)
                        print(f"Updated: {folder_name}/{file}")
                        updated_count += 1

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

if __name__ == "__main__":
    changed = sync_folders()
    if changed:
        git_commit_and_push()
    else:
        print("No changes detected in synced folders.")
