# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

import httpx;
from httpx import RequestError;
from markdownify import MarkdownConverter;

from sbercode.colors import *;

WEB_FETCH_FUNCTION = {
    "name": "web_fetch",
    "description": "Сделать запрос к веб ресурсу, и получить ответ в markdown формате",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL-адрес для запроса"
            },
            "timeout": {
                "type": "integer",
                "description": "Таймаут запроса в секундах",
                "default": 10
            },
            "show_source": {
                "type": "boolean",
                "description": "Показывает оригинальный исходный код страницы в html",
                "default": False
            }
        },
        "required": ["url"]
    },
    "few_shot_examples": [
        {
            "request": "Получить главную страницу example.com",
            "params": {
                "url": "https://example.com"
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "status_code": {
                "type": "integer",
                "description": "HTTP-код ответа"
            },
            "content": {
                "type": "string",
                "description": "Содержимое ответа"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
};

class LinkNoTitleConverter(MarkdownConverter):
    def convert_a(self, el, text, parent_tags):
        # Принудительно удаляем атрибут title, если он есть
        el.attrs.pop('title', None);
        # Вызываем стандартную логику markdownify для ссылок
        return super().convert_a(el, text, parent_tags);

def markdownify(html, **options):
    return LinkNoTitleConverter(**options).convert(html);

class WebFetch:
    desc = WEB_FETCH_FUNCTION;
    def run(self, args):
        url = args["url"];
        timeout = args.get("timeout", 10);

        with httpx.Client(http2=True, follow_redirects=True, timeout=timeout) as client:
            response = client.get(url);
        print(f"  {WHITE}{response.status_code} {response.reason_phrase}");
        text = response.text;
        if not args.get("show_source"):
            text = markdownify(text);
        return {
            "status_code": response.status_code,
            "content": text
        }

    def print_args(self, args):
        src = "";
        if args.get("show_source"):
            src = f"{YELLOW} (show_source=True)";
        print(f"  {YELLOW}+ Web fetch {WHITE}{args['url']}{src}{RESET}")
