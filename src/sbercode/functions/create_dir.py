# SPDX-License-Identifier: 0BSD
# Copyright 2026 GigaChat-3-Ultra

import os
from sbercode.colors import *

CREATE_DIR_FUNCTION = {
    "name": "create_dir",
    "description": "Создать директорию",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Путь к директории, которую нужно создать"
            }
        },
        "required": ["path"]
    },
    "few_shot_examples": [
        {
            "request": "Создай папку new_folder",
            "params": {
                "path": "new_folder"
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Сообщение об успешном создании"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
}

class CreateDir:
    desc = CREATE_DIR_FUNCTION

    def run(self, args):
        path = args["path"]
        os.makedirs(path, exist_ok=True)
        return {"status": f"Directory '{path}' created successfully."}

    def print_args(self, args):
        print(f"  {YELLOW}+ Mkdir {WHITE}{args['path']}{RESET}")

    def describe(self, args):
        return f"Create dir {args['path']}";
