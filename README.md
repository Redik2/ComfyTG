Этот проект является приложением, связывающее ComfyUI и Telegram на сколько это возможно и на сколько мне это удобно

# Использование

Для использования необходима **настройка**
в телеграм боте используется команда:

```
/txt2img model name --parameter1 
```

## Настройка

В файлах проекта есть `config.json`, туда нужно записать токен бота и указать абсолютный путь до места, куда сохраняются изображения из ComfyUI(в json может понадобится использовать `//` взамен `/`)

## Создание нового промпта

Для создания нового промпта нужно положить модель в `/models`, и схему к модели в `/schemas`
На пример:

```md
/models
    example.json
    cool_model_123.json
/schemas
    example.json
    cool_model_123.json
```

### Создание модели

Новый промпт, экспортированный из ComfyUI в качестве api
Он не должен подвергаться никаким изменениям после экспорта

### Создание схемы

Схемы - это **json** файлы, которые представляют из себя словарь типа `"параметр": {"type": "тип параметра", "path": "путь"}` и нужен для удобного доступа к параметрам модели

**Параметр** - название параметра, без пробелов(не обязательно повторяет название параметра в модели), который в будущем можно будет указывать и изменять через интерфейс бота

**Тип параметра** - строка, число, или что иное. Возможные варианты:

```
str
int
float
bool
```

**Путь** - строка типа `path/to/parameter`. Путь строится в зависимости от модели и отображает путь до параметра

Пример:

#### Модель

```json
.  .  .

    "7": {
        "inputs": {
            "text": "some really cool prompt",
            "clip": [
                "1",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
          "title": "CLIP Text Encode (Prompt)"
        }
    },

.  .  .
```

#### Схема

```json
{
    "positive_prompt": {
        "type": "str",
        "path": "7/inputs/text"
    }
}
```

В параметр `"chat_id"` всегда передается id чата, куда нужно отправить изображение. Он обязательно должен быть в схеме, его тип `str` и вести он должен к `Save Image/image_prefix`

В параметры `"rseed0"` - `"rseed999"` всегда передается случайный сид генерации. Он не обязательно должен быть в схеме, но если он есть, то его тип обязан быть `int`
