# SPDX-License-Identifier: 0BSD
# Copyright 2026 GigaChat-3-Ultra

import os
import shutil
from sbercode.colors import *

REMOVE_DIR_FUNCTION = {
    "name": "remove_dir",
    "description": "Удалить директорию",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Путь к директории, которую нужно удалить"
            }
        },
        "required": ["path"]
    },
    "few_shot_examples": [
        {
            "request": "Удалить папку old_data",
            "params": {
                "path": "old_data"
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Сообщение об успешном удалении"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
}

class RemoveDir:
    desc = REMOVE_DIR_FUNCTION

    def run(self, args):
        path = args["path"]
        # Запрос подтверждения у пользователя
        i = input(f"  {BRED}[!!!] ВНИМАНИЕ! Удаление директории! Вы точно хотите удалить {WHITE}'{path}'{BRED} и {BOLD}всё её содержимое?{RESET} [y/N] ").strip().lower()
        if i != "y":
            return {"error": "User denied execution of this command"}

        # Используем shutil.rmtree для удаления директорий с содержимым
        shutil.rmtree(path)
        return {"status": f"Directory '{path}' removed successfully."}

    def print_args(self, args):
        print(f"  {YELLOW}+ Remove dir {WHITE}{args['path']}{RESET}")
