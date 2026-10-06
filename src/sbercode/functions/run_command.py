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
                "description": "Timeout в секундах. Рекомендуемое значение - 10 секунд"
            },
            "stdin": {
                "type": "string",
                "description": "Строка, которая будет отправлена в stdin"
            }
        },
        "required": [ "command", "timeout" ]
    },
    "few_shot_examples": [
        {
            "request": "Проверим версию python",
            "params": {
                "command": "python -v",
                "timeout": 10
            }
        }
    ],
    "return_parameters": {
        "type": "object",
        "properties": {
            "stdout": { "type": "string" },
            "stderr": { "type": "string" },
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
        stdout, stderr = cmd.communicate(input=args.get("stdin"), timeout=args["timeout"]);
        print(stdout, end="");
        print(stderr, end="");
        return { "stdout": stdout, "stderr": stderr };
    def print_args(self, args):
        print("\n  " + WHITE + "$ " + args["command"] + RESET);
