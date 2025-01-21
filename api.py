import requests
import json

COMFY_UI_URL = "http://127.0.0.1:8188"


def send_prompt(file: str, positive: str, negative: str):
    prompt = json.dumps({"prompt": json.load(open(file))})
    print(prompt)
    url = f"{COMFY_UI_URL}/prompt"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=prompt)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    send_prompt("Test.json", "", "")