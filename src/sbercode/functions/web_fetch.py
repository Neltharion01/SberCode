# SPDX-License-Identifier: 0BSD
# Copyright 2026 GigaChat-3-Ultra

import httpx
from httpx import RequestError

from sbercode.colors import *

WEB_FETCH_FUNCTION = {
    "name": "web_fetch",
    "description": "Выполнить HTTP-запрос к веб-ресурсу",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL-адрес для запроса"
            },
            "method": {
                "type": "string",
                "description": "HTTP-метод (GET, POST, PUT, DELETE, HEAD, PATCH)",
                "default": "GET"
            },
            "headers": {
                "type": "object",
                "description": "HTTP-заголовки в формате {\"Header-Name\": \"value\"}",
                "additionalProperties": {
                    "type": "string"
                }
            },
            "data": {
                "type": "string",
                "description": "Тело запроса (для POST, PUT, PATCH)"
            },
            "timeout": {
                "type": "integer",
                "description": "Таймаут запроса в секундах",
                "default": 30
            },
            "follow_redirects": {
                "type": "boolean",
                "description": "Следовать ли редиректам",
                "default": True
            }
        },
        "required": ["url"]
    },
    "few_shot_examples": [
        {
            "request": "Получить главную страницу example.com",
            "params": {
                "url": "https://example.com",
                "method": "GET"
            }
        },
        {
            "request": "Проверить заголовки google.com",
            "params": {
                "url": "https://google.com",
                "method": "HEAD"
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Статус выполнения"
            },
            "status_code": {
                "type": "integer",
                "description": "HTTP-код ответа"
            },
            "headers": {
                "type": "object",
                "description": "Заголовки ответа"
            },
            "content": {
                "type": "string",
                "description": "Тело ответа"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
};

class WebFetch:
    desc = WEB_FETCH_FUNCTION;
    def run(self, args):
        method = args.get("method", "GET").upper()
        url = args["url"]
        timeout = args.get("timeout", 30)
        allow_redirects = args.get("follow_redirects", True)
        headers = args.get("headers", {})
        data = args.get("data")

        with httpx.Client(http2=True, follow_redirects=allow_redirects, timeout=timeout) as client:
            response = client.request(
                method=method,
                url=url,
                headers=headers,
                data=data.encode() if data else None
            )
        print(f"  {WHITE}{response.status_code} {response.reason_phrase}");
        return {
            "status": "success",
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text
        }

    def print_args(self, args):
        method = args.get("method", "GET").upper()
        print(f"  {WHITE}{method} {args['url']}{RESET}")
        if args.get("headers"):
            print(f"  {WHITE}Headers: {args['headers']}{RESET}")
        if args.get("data"):
            print(f"  {WHITE}Data: {args['data']}{RESET}")
