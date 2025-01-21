import requests
import json
import schemas

COMFY_UI_URL = "http://127.0.0.1:8188"


def send_prompt(model_name: str, values: dict):
    model = json.load(open(f"models/{model_name}.json", "r"))
    schema = json.load(open(f"schemas/{model_name}.json", "r"))
    
    for key, value in values.items():
        schemas.set_value(schema, model, key, value)
    
    if "rseed" in schema.keys():
        schemas.set_seed(schema, model)

    prompt = json.dumps({"prompt": model})


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
    send_prompt("example", {"prompt": "1girl, casual clothing"})