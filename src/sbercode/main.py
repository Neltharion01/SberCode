# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

import os;
import json;
from pathlib import Path;
from threading import Thread;
from time import sleep

from sbercode.api import SberChat;
from sbercode.colors import *;
from sbercode.functions import Functions;

def make_cfgdir(home):
    dir = home;
    for seg in ".config", "sbercode":
        dir /= seg;
        if not dir.exists():
            os.mkdir(dir);
    return dir;

def sum_chunks(c1, c2):
    result = c1.copy();
    for key, value in c2.items():
        if key == "content":
            result["content"] = result.get("content", "") + value;
        else:
            result[key] = value;
    return result;

def main():
    home = Path(os.environ["HOME"]);
    cfgdir = make_cfgdir(home);
    cfgfile = open(cfgdir / "config.json");
    cfg = json.load(cfgfile);
    cfgfile.close();

    token = cfg["token"];
    model = cfg["model"];
    cwd = os.getcwd();

    sber_chat = SberChat(token, model);
    sber_chat.functions = Functions.serialize();

    # Refresh access token in background
    Thread(target=sber_chat.get_token).start();

    INIT_PROMPT = f"""\
Ты - SberCode, ассистент для разработки. Ты можешь работать с кодом, используя инструменты, такие как run_command, read_file, write_file, edit_file
Используемая модель: {model}
Рабочая директория: {cwd}
Пользователь разрешил работать с файлами проекта. За пределы папки проекта выходить нельзя
""";
    history = [{ "role": "system", "content": INIT_PROMPT }];

    print(f"");
    print(f"  Welcome to {BGREEN}SberCode{RESET}! Current model:{BGREEN}", model, RESET);
    print(f"  Press {BBLUE}Ctrl+C and Enter{RESET} or {BBLUE}Ctrl+d{RESET} to exit");
    print(f"");

    try:
        # Main loop
        while True:
            msg = input(f"  {YELLOW}+ Your message:{RESET} ");
            history.append({ "role": "user", "content": msg });
            # Function calling loop
            while True:
                res = sber_chat.complete_stream(history);
                first_chunk = next(res);
                if first_chunk.get("finish_reason") != "function_call":
                    assembled = first_chunk["delta"];
                    print(f"  {YELLOW}+ Response{RESET}\n");
                    print("  " + first_chunk["delta"]["content"], end="", flush=True);
                    for chunk in res:
                        print(chunk["delta"]["content"], end="", flush=True);
                        assembled = sum_chunks(assembled, chunk["delta"]);
                    print("\n");
                    history.append(assembled);
                    break;
                else:
                    # Drain the stream
                    for chunk in res:
                        print("[WARN] leftover chunk in function call:", chunk);
                    delta = first_chunk["delta"];
                    history.append(delta);
                    fncall = delta["function_call"];
                    fnres = Functions.call(fncall["name"], fncall["arguments"]);
                    history.append({ "role": "function", "name": fncall["name"], "content": json.dumps(fnres) });

    except (EOFError) as e:
        print("exit");
