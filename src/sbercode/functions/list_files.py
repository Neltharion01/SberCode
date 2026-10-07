# SPDX-License-Identifier: 0BSD
# Copyright 2026 GigaChat-3-Ultra

import os
from sbercode.colors import *

LIST_FILES_FUNCTION = {
    "name": "list_files",
    "description": "Вывести список файлов и директорий",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Путь к директории, содержимое которой нужно вывести"
            }
        },
        "required": ["path"]
    },
    "few_shot_examples": [
        {
            "request": "Покажи файлы в текущей директории",
            "params": {
                "path": "."
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "description": "Список файлов и директорий",
                "additionalProperties": {
                    "type": "string"
                }
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
}

class ListFiles:
    desc = LIST_FILES_FUNCTION

    def run(self, args):
        data = os.listdir(args["path"])
        return {"files": data}

    def print_args(self, args):
        print(f"  {YELLOW}+ List files {WHITE}{args['path']}{RESET}")
