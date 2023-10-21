import openai
import json
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

types = [
    {
        "type": "heading-1",
        "content": ""
    },
    {
        "type": "heading-2",
        "content": ""
    },
    {
        "type": "heading-3",
        "content": ""
    },
    {
        "type": "heading-4",
        "content": ""
    },
    {
        "type": "text",
        "content": ""
    },
    {
        "type": "list",
        "list": []
    },
    {
        "type": "num-list",
        "list": []
    },
    {
        "type": "todo-list",
        "list": [
            {
                "done": False,
                "content": ""
            }
        ]
    },
    {
        "type": "code",
        "language": "",
        "content": ""
    },
    {
        "type": "caption",
        "content": "",
        "author": ""
    },
]

typesDescription = """ Список текстовых блоков:

1. heading-1: Заголовок 1 уровня, контент в поле "content".
2. heading-2: Заголовок 2 уровня, контент в поле "content".
3. heading-3: Заголовок 3 уровня, контент в поле "content".
4. heading-4: Заголовок 4 уровня, контент в поле "content".
5. text: Просто текст, контент в поле "content".
6. list: Список, элементы в массиве в поле "list".
7. num-list: Нумерованный список, аналогичен "list".
8. todo-list: Туду-лист, элементы с полями "done" (выполнено или нет) и "content" (содержание задачи).
9. code: Блок кода, с полями language - в него записывается язык программирования и content - контент.
9. caption: Цитата с "content" и опциональным полем "author" для имени автора.

Эти текстовые блоки помогают организовать информацию в документе.
"""

instruction = ("Твоя задача написать текст, по запросу пользователя. Текст нужно писать в формате JSON по следующим "
               "правилам: ") + str(
    types) + " \n " + typesDescription + ("\n  Далее я буду отправлять тебе запросы пользователя. В ответ отправляй "
                                          "только сгенерированный тобой текст и больше ничего. Ответ должен "
                                          "представлять собой JSON массив с готовыми текстовыми блоками. В ответе "
                                          "ТОЛЬКО ЭТОТ JSON И БОЛЬШЕ НИЧЕГО!!! Так как это JSON ключи и значения "
                                          "должны быть в двойных кавычках. Вот пример твоего ответа: \n"
                                          '['
                                          '		{'
                                          '			"type": "heading-1",'
                                          '			"content": "Охуеть бля"'
                                          '		},'
                                          '		{'
                                          '			"type": "text",'
                                          '			"content": "Вот короче тут крутой текст вот собственно так вот"'
                                          '		},'
                                          '		{'
                                          '			"type": "list",'
                                          '			"list": ['
                                          '				"Первый элемент",'
                                          '				"Второй",'
                                          '				"Так далее"'
                                          '			]'
                                          '		},'
                                          '		{'
                                          '			"type": "num-list",'
                                          '			"list": ['
                                          '				"Первый элемент",'
                                          '				"Второй",'
                                          '				"Так далее"'
                                          '			]'
                                          '		},'
                                          '		"type": "todo-list",'
                                          '			"list": ['
                                          '				{'
                                          '	        "done": true,'
                                          '					"content": "Помыть попу"'
                                          '				},'
                                          '				{'
                                          '	        "done": false,'
                                          '					"content": "Почистить хуй"'
                                          '				},'
                                          '			]'
                                          '	]'
                                          '')

openai.api_key = ""

messages = [
    {"role": "system", "content": instruction},
]


def generateText(text):
    messages.append({
        "role": "user",
        "content": text
    })

    print("Генерирую ответ")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    message = response.choices[0].message.content

    print(message)
    return message


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Item(BaseModel):
    text: str


@app.post("/gpt/")
async def say_hello(item: Item):
    response = generateText(item.text)
    return {"success": True, "response": json.loads(response)}
