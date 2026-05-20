import sys
import os
sys.path.append(os.getcwd())
from affiliate.accesstrade.campaigns import get_campaigns
from affiliate.accesstrade.direct_link import get_direct_link_script

output_dir = "generated_sites"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Dang lay danh sach campaigns...")
campaigns = get_campaigns(approval="successful", limit=50)
print("Tim thay", len(campaigns), "campaigns")

for idx, camp in enumerate(campaigns, 1):
    camp_id = camp['id']
    camp_name = camp['name']
    print(f"[{idx}/{len(campaigns)}] Dang xu ly: {camp_name}")
    try:
        result = get_direct_link_script(camp_id)
        safe_name = "".join(c for c in camp_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        file_path = os.path.join(output_dir, f"{safe_name}_{camp_id}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result['embed_html'])
        print(f"   OK: {file_path}")
    except Exception as e:
        print(f"   LOI: {e}")

print("HOAN TAT.")