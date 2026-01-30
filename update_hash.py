import json, hashlib, os, glob, sys

# ✅ 네 .img들이 있는 폴더 (로컬 PC 경로)
IMG_DIR = r"C:\Users\아정\Desktop\스킬해시값"

# ✅ 레포 안 skills.json 경로 (보통 루트에 있음)
JSON_PATH = "skills.json"   # 만약 파일명이 '스킬스.json'이면 그걸로 바꿔줘

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

img_paths = sorted(glob.glob(os.path.join(IMG_DIR, "*.img")))
if not img_paths:
    print(f"[ERR] No .img files found in: {IMG_DIR}", file=sys.stderr)
    sys.exit(1)

hash_by_id = {}
for p in img_paths:
    base = os.path.basename(p)
    _id, _ = os.path.splitext(base)
    hash_by_id[_id] = sha256_file(p)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

skills = data.get("skills")
if not isinstance(skills, list):
    print('[ERR] skills.json must contain {"skills": [...]}', file=sys.stderr)
    sys.exit(1)

updated = 0
for s in skills:
    sid = s.get("id")
    if sid in hash_by_id:
        s["sha256"] = hash_by_id[sid]
        updated += 1

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[OK] Updated sha256 for {updated} skill items.")
