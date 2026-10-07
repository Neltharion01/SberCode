# SPDX-License-Identifier: 0BSD
# Copyright 2026 GigaChat-3-Ultra

import os
from sbercode.colors import *

REMOVE_FILE_FUNCTION = {
    "name": "remove_file",
    "description": "Удалить файл",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Имя файла, который нужно удалить"
            }
        },
        "required": ["file_name"]
    },
    "few_shot_examples": [
        {
            "request": "Удалить файл temp.txt",
            "params": {
                "file_name": "temp.txt"
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

class RemoveFile:
    desc = REMOVE_FILE_FUNCTION

    def run(self, args):
        file_name = args["file_name"]
        # Запрос подтверждения у пользователя
        i = input(f"  {BRED}[!!!] ВНИМАНИЕ! Удаление файла! Вы точно хотите удалить {WHITE}'{file_name}'{BRED}?{RESET} [y/N] ").strip().lower()
        if i != "y":
            return {"error": "User denied execution of this command"}

        os.remove(file_name)
        return {"status": f"File '{file_name}' removed successfully."}

    def print_args(self, args):
        print(f"  {YELLOW}+ Remove file {WHITE}{args['file_name']}{RESET}")
