import requests
import json
import schemas
from copy import deepcopy

COMFY_UI_URL = "http://127.0.0.1:8188"

token = json.load(open("config.json", "r"))["openrouter_token"]

def send_prompt(model_name: str, values: dict, natural_language: str, history: list[dict]):
    model = json.load(open(f"models/{model_name}.json", "r"))
    schema = json.load(open(f"schemas/{model_name}.json", "r"))
    
    positive, negative, width, height = generate_prompt(model, schema, values, natural_language, history)

    prompt = json.dumps({"prompt": model})


    url = f"{COMFY_UI_URL}/prompt"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=prompt)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        return positive, negative, width, height
    

def generate_prompt(model: dict, schema: dict, values: dict, natural_language: str, history: list[dict]):
    history.append({"role": "user", "content": natural_language})

    
    messages = deepcopy(history)
    messages[-1]['content'] += '\nP.S. ' + values['user_prompt']
    print(json.dumps(messages[1:], indent=4, ensure_ascii=False))

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "deepseek/deepseek-chat:free",
        "temperature": 1,
        "messages": messages
        
    })
    )
    content: str = response.json()['choices'][0]['message']['content']
    history.append({'role': 'assistant', 'content': content})
    print(json.dumps(response.json(), indent=4, ensure_ascii=False).replace("\\n", "\n").replace("\\\"", "\""))

    answer: dict = json.loads(content.removeprefix("```json").removesuffix("```"))
    width = answer.get("width", 256)
    height = answer.get("height", 256)
    positive = answer.get("positive", "")
    negative = answer.get("negative", "")

    width = int(width) // 64 * 64
    height = int(height) // 64 * 64

    try:
        values['positive'] = positive
        values['negative'] = negative
        value['width'] = width
        value['height'] = height
    except:
        pass

    for key, value in values.items():
        if key == "user_prompt":
            continue
        try:
            schemas.set_value(schema, model, key, value)
        except KeyError as e:
            print(f"Ключ {e} не указан в схеме, игнорирование")
    
    schemas.set_seed(schema, model)
    return positive, negative, width, height

if __name__ == "__main__":
    send_prompt("example", {"prompt": "1girl, casual clothing"})