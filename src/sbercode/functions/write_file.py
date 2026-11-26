# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

from sbercode.colors import *;

WRITE_FILE_FUNCTION = {
    "name": "write_file",
    "description": "Записать файл",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Имя для файла, который нужно записать"
            },
            "contents": {
                "type": "string",
                "description": "Содержимое файла"
            },
            "overwrite": {
                "type": "boolean",
                "description": "Если True, перезапишет файл, если он существует",
                "default": False
            }
        },
        "required": [ "file_name", "contents" ]
    },
    "few_shot_examples": [
        {
            "request": "Создаём helloworld.py",
            "params": {
                "file_name": "helloworld.py",
                "contents": "print(\"hello world\")\n"
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

class WriteFile:
    desc = WRITE_FILE_FUNCTION;
    def run(self, args):
        mode = "x"
        if args.get("overwrite", False):
            mode = "w"
        try:
            f = open(args["file_name"], mode);
            f.write(args["contents"]);
            if args["contents"][-1] != "\n":
                f.write("\n");
            f.close();
            return { "status": "success" };
        except FileExistsError:
            return { "error": f"File '{args['file_name']}' already exists. Use overwrite=True to replace it." }
    def print_args(self, args):
        print(f"  {YELLOW}+ Write file {WHITE}{args["file_name"]}{RESET}");
        for line in args["contents"].splitlines():
            print(BGREEN + "+ " + RESET + line);
