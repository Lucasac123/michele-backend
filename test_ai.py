import requests
import json

API_URL = "http://127.0.0.1:8000"

def test_interpret():
    prompt = "Uma etiqueta do Mickey para o caderno do Joao"
    print(f"Sending prompt: {prompt}")
    
    response = requests.post(f"{API_URL}/generate", json={"prompt": prompt})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_interpret()
