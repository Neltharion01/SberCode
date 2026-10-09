# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

from sbercode.colors import *;

EDIT_FILE_FUNCTION = {
    "name": "edit_file",
    "description": "Редактировать файл",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Имя для файла, который нужно отредактировать"
            },
            "replace_from": {
                "type": "string",
                "description": "Строка, которую нужно заменить"
            },
            "replace_to": {
                "type": "string",
                "description": "На что заменяем"
            }
        },
        "required": [ "file_name", "contents" ]
    },
    "few_shot_examples": [
        {
            "request": "Починим импорты",
            "params": {
                "file_name": "code.py",
                "replace_from": "import requests\n",
                "replace_to": "import requests\nimport json\n"
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Результат выполнения операции"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
};

class EditFile:
    desc = EDIT_FILE_FUNCTION;

    def run(self, args):
        f = open(args["file_name"], "r+");
        data = f.read();
        if args["replace_from"] not in data:
            print(f"  {BRED}[X] Error: substring not found{RESET}");
            return { "error": "substring not found" };
        data = data.replace(args["replace_from"], args["replace_to"]);
        f.seek(0);
        f.truncate();
        f.write(data);
        f.close();
        return { "status": "success" };

    def print_args(self, args):
        print(f"  {YELLOW}+ Edit file {WHITE}{args["file_name"]}{RESET}");
        for line in args["replace_from"].splitlines():
            print(BRED + "- " + RESET + line);
        for line in args["replace_to"].splitlines():
            print(BGREEN + "+ " + RESET + line);

    def describe(self, args):
        return f"Edit file {args['file_name']}";
