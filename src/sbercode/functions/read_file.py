# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

from sbercode.colors import *;

READ_FILE_FUNCTION = {
    "name": "read_file",
    "description": "Прочитать файл",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Имя файла, который нужно прочитать"
            }
        },
        "required": [ "file_name" ]
    },
    "few_shot_examples": [
        {
            "request": "Прочитаем helloworld.py",
            "params": {
                "file_name": "helloworld.py"
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "contents": {
                "type": "string",
                "description": "Содержимое файла"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
};

class ReadFile:
    desc = READ_FILE_FUNCTION;

    def run(self, args):
        f = open(args["file_name"]);
        data = f.read();
        f.close();
        return { "contents": data };

    def print_args(self, args):
        print(f"  {YELLOW}+ Read file {WHITE}{args["file_name"]}{RESET}");

    def describe(self, args):
        return f"Read file {args['file_name']}";
