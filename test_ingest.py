import requests
import os

API_URL = "http://127.0.0.1:8000"
TEST_ASSETS_DIR = os.path.abspath("../test_assets")

def test_ingestion():
    print(f"Testing ingestion for directory: {TEST_ASSETS_DIR}")
    response = requests.post(f"{API_URL}/ingest", params={"directory_path": TEST_ASSETS_DIR})
    print(f"Ingest Status: {response.status_code}")
    print(f"Ingest Response: {response.json()}")

    # List Assets
    response = requests.get(f"{API_URL}/assets")
    print(f"Assets List Status: {response.status_code}")
    print(f"Assets Found: {len(response.json())}")
    for asset in response.json():
        print(f" - {asset['name']} ({asset['asset_type']}) Tags: {[t['name'] for t in asset['tags']]}")

if __name__ == "__main__":
    test_ingestion()
