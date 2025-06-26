import json
from pathlib import Path

ORG_DATA_PATH = Path(__file__).parent.parent / "data" / "org_basic.json"

def load_org_basic():
    with open(ORG_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_role_prompt(user_text):
    org = load_org_basic()
    base = (
        f"你是「{org['name']}」的智能助理，宗旨：{org['mission']}。\n"
        f"協會資訊：{org['projects']}。\n"
        "請專業且親切地回答使用者問題。\n"
        f"使用者提問：{user_text}"
    )
    return base