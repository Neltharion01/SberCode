# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

import subprocess;

from sbercode.colors import *;

RUN_COMMAND_FUNCTION = {
    "name": "run_command",
    "description": "Выполнить команду в bash",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Команда, которую нужно выполнить"
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout в секундах. Если background задан как true, то timeout игнорируется",
                "default": 10
            },
            "stdin": {
                "type": "string",
                "description": "Строка, которая будет отправлена в stdin"
            },
            "background": {
                "type": "boolean",
                "description": "Если True, команда будет запущена в фоновом режиме"
            }
        },
        "required": [ "command" ]
    },
    "few_shot_examples": [
        {
            "request": "Проверим версию python",
            "params": {
                "command": "python -v"
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
            "stdout": { "type": "string" },
            "stderr": { "type": "string" },
            "exit_code": {
                "type": "integer",
                "description": "Код завершения"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
};

class RunCommand:
    desc = RUN_COMMAND_FUNCTION;
    def run(self, args):
        if args["command"].startswith("rm"):
            i = input(f"  {BRED}[!!!] ВНИМАНИЕ! ОПАСНАЯ КОМАНДА! Вы точно хотите её выполнить?{RESET} [y/N] ").strip().lower();
            if i != "y":
                return { "error": "User denied execution of this command" };
        cmd = subprocess.Popen(["bash", "-c", args["command"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True);
        if args.get("background"):
            return { "status": "command spawned successfully" };
        stdout, stderr = cmd.communicate(input=args.get("stdin"), timeout=args.get("timeout", 10));
        print(stdout, end="");
        print(stderr, end="");
        code = cmd.wait();
        return { "status": "success", "stdout": stdout, "stderr": stderr, "exit_code": code };
    def print_args(self, args):
        if args.get("background"):
            bg = " &";
        else:
            bg = "";
        print("  " + WHITE + "$ " + args["command"] + bg + RESET);
