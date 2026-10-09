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
from sbercode.history import History;

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

    try:
        accfile = open(cfgdir / "access_token.json");
        sber_chat.access_token = json.load(accfile);
        accfile.close();
    except FileNotFoundError: pass;

    def acc_on_save(access_token):
        accfile = open(cfgdir / "access_token.json", "w");
        json.dump(access_token, accfile);
        accfile.close();
    # Set token on_save function
    sber_chat.token_on_save = acc_on_save;
    # Refresh access token in background
    Thread(target=sber_chat.get_token).start();

    INIT_PROMPT = f"""
        Ты - SberCode, ассистент для разработки. Ты можешь работать с кодом, используя инструменты, такие как run_command, read_file, write_file, edit_file
        Используемая модель: {model}
        Рабочая директория: {cwd}
        Пользователь разрешил работать с файлами проекта. За пределы папки проекта выходить нельзя
    """;
    history = History.load();
    if not history.get():
        history.append({ "role": "system", "content": INIT_PROMPT });
    sber_chat.session_id = history.get_session_id();

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
                res = sber_chat.complete_stream(history.get());
                response_printed = False;
                assembled = {};
                for chunk in res:
                    if chunk.get("finish_reason") == "error":
                        print(f"  {BRED}[X]Failed to generate response: unknown error{RESET}");
                        print(f"  {BRED}   Terminating session...{RESET}");
                        return;
                    if chunk["delta"]["content"] and not response_printed:
                        print(f"  {YELLOW}+ Response{RESET}\n\n  ", end="", flush=True);
                        response_printed = True;
                    print(chunk["delta"]["content"], end="", flush=True);
                    assembled = sum_chunks(assembled, chunk["delta"]);
                if response_printed: print("\n");
                history.append(assembled);

                if "function_call" in assembled:
                    fncall = assembled["function_call"];
                    fnres = Functions.call(fncall["name"], fncall["arguments"]);
                    history.append({ "role": "function", "name": fncall["name"], "content": json.dumps(fnres, ensure_ascii=False) });
                else:
                    # Exit function loop, input next message
                    break;

    except (KeyboardInterrupt, EOFError) as e:
        print("exit");

    finally:
        history.close();
